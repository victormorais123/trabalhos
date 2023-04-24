import itertools
import math
import re
from typing import List, Tuple


class EvalFormula:
    token_regexes = [
        (r'[A-Za-z][A-Za-z0-9]*', 'LITERAL'),  # Variables and constants
        (r'&', 'AND'),  # Conjunction symbol
        (r'\|', 'OR'),  # Disjunction symbol
        (r'~', 'NOT'),  # Negation symbol
        (r'\(', 'LPAREN'),  # Left parenthesis
        (r'\)', 'RPAREN'),  # Right parenthesis
        (r'<->', 'IFF'),  # Biconditional symbol
        (r'->', 'IMPLIES'),  # Conditional symbol
        (r'\!', 'NOT'),  # Alternative negation symbol
        (r'\b(true|false)\b', 'LOGICAL_CONSTANT'),  # True and false constants
    ]

    def __init__(self, formula):
        # if not self._is_cnf(formula):
        #     # raise ValueError(f'formula "{formula}" is not in CNF format.')
        #     print(f'formula "{formula}" is not in CNF format. Converting...')
        #     self._to_cnf(formula)
        self.cnf_formula = formula
        self.cnf_equiv = None
        self.tokens = []
        self.clauses = []
        self.literals = []
        # self.table_rows = []
        self.truth_values = {}

        # self._new_parser()

    def _find_matching_parenthesis(self, start):
        count = 1
        for pos in range(start + 1, len(self.cnf_formula)):
            if self.cnf_formula[pos] == "(":
                count += 1
            elif self.cnf_formula[pos] == ")":
                count -= 1
            if count == 0:
                return pos
        raise ValueError("Mismatched parenthesis in formula")

    def _adj_unary(self, cl):
        if len(cl) != 2:
            raise ValueError('Clause is not an unary one.')

    def _adj_binary(self, cl):
        lits = [idx for idx, c in enumerate(cl) if c.isalpha()]
        op = [idx for idx, c in enumerate(cl) if c in ['|', '&']]

        out = []
        if len(lits) == 2 and len(op) == 1:
            out.append('or' if cl[op.pop()] == '|' else 'and')
            out.append([cl[x] for x in lits])

        return out

    def _new_parser(self):
        # stack = [[]]
        tokens = [t for t in re.sub(r'\s+', '', self.cnf_formula)]
        variables = [v for v in tokens if v not in ['(', ')', 'AND', 'OR', 'NOT', '&', '|', '~']]

        fml = '(P|Q) & R'
        # fml = '~A|B'

        out_fml = re.sub(r'[\s+]?&[\s+]?', ' AND ', fml)
        pattern = re.compile(r'\(~?(\w+)[\s+]?(&|AND|and|OR|or|\|)[\s+]?(\w)\)|(\w+)')
        match = pattern.findall(out_fml)
        out = []
        for x in match:
            inn = [y for y in x if y != '']
            out.append(inn)

        for idx, y in enumerate(out):
            k = self._adj_binary(y)
            out[idx] = k

        rst = list(match)

        regex = r"\((\w+)[\s+]?(&|AND|and|OR|or|\|)[\s+]?(\w)\)|(\w+)"
        test_str = "(P|Q) AND R"
        matches = re.finditer(regex, test_str)
        for matchNum, match in enumerate(matches, start=1):
            print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                                end=match.end(), match=match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                start=match.start(groupNum),
                                                                                end=match.end(groupNum),
                                                                                group=match.group(groupNum)))

        pos = 0
        clauses = []
        while pos < len(self.cnf_formula):
            char = self.cnf_formula[pos]
            if char == "(":
                clause_end = self._find_matching_parenthesis(pos)
                sub_formula = self.cnf_formula[pos + 1:clause_end]
                # sub_clauses = self._new_parser(sub_formula)
                # clauses += sub_clauses
                pos = clause_end + 1
            elif char == ")":
                raise ValueError("Mismatched parenthesis in formula")
            else:
                var, pos = self._parse_variable(formula, pos)
                if pos < len(self.cnf_formula) and self.cnf_formula[pos] == "&":
                    pos += 1
                if var not in self.vars:
                    self.vars[var] = len(self.vars) + 1
                    self.rev_vars[len(self.vars)] = (var, True)
                clause = [self.vars[var] if not neg else -self.vars[var] for (var, neg) in self.rev_vars.values()]
                if not var:
                    clause += [0]
                clauses.append(clause)

        return clauses

        # if tokens[pos] in ['NOT', '~']:
        #     stack[-1].append(['neg', tokens[pos + 1]])
        #     pos += 2

        # if fml[pos] == "(":
        #     stack.append([])
        # elif fml[pos] == ")":
        #     inner = stack.pop()
        #     stack[-1].append(inner)
        # else:
        #     if len(stack) > 0:
        #         stack[-1].append(fml[pos])
        #     else:
        #         stack.append(fml[pos])
        #
        # pos += 1

    @property
    def number_of_rows(self) -> int:
        return len(list(self.truth_values.values())[0])

    @property
    def number_of_columns(self) -> int:
        return len(self.clauses)

    def tokenize(self):
        # self._remove_bi_implies()
        self._remove_implies()
        formula = self.cnf_formula

        while formula:
            actual_token = self._make_clause_token(formula)
            formula = formula[len(actual_token[0]):].lstrip()
            self.tokens.append(actual_token)

        self._make_literals()
        self._make_clauses()
        self._fill_table_literals()

    def print_table(self):
        str_head = f'formula: {self.cnf_equiv} == {self.cnf_formula}' if self.cnf_equiv \
            else f'formula: {self.cnf_formula}'
        print(str_head)
        larger_clause = max([len(x) for x in self.clauses]) + 2
        tbl_format = '|'.join([f'{{:^{larger_clause}}}'] * (len(self.clauses) + 1))

        table_header = tbl_format.format(*(self.clauses + ['W']))
        print(table_header)
        print('-' * len(table_header))

        table_rows = [list(x) for x in zip(*self.truth_values.values())]

        # connective_str = r'&' if re.match(r'&', self.cnf_formula) else r'\|'
        connective_str = r'&' if re.match(r'(.*)&(.*)', self.cnf_formula) else r'\|'

        formula_to_eval = [re.sub(r'\s', '', c) for c in re.split(connective_str, self.cnf_formula)]
        idx_to_eval = [idx for idx, cls in enumerate(self.clauses) if cls in formula_to_eval]

        for i, combination in enumerate(table_rows):
            partials = [combination[i] for i in idx_to_eval]
            result = all(partials) if connective_str == '&' else any(partials)
            compact = ['T' if c else 'F' for c in combination + [result]]
            table_row = tbl_format.format(*compact)
            print(table_row)

    def eval(self):
        for cl in [clause for clause in self.clauses if clause not in self.literals]:
            if cl.startswith('~'):
                active_clause = cl[1:]
                if active_clause in self.truth_values.keys():
                    self.truth_values[cl] = [not x for x in self.truth_values.get(active_clause)]
            else:
                self.truth_values[cl] = self._eval_clause(cl)

    def _remove_bi_implies(self):
        match = re.search(r'(.*)<->(.*)', self.cnf_formula)
        if match:
            a, b = match.groups()
            self.cnf_equiv = self.cnf_formula
            self.cnf_formula = ''.join(['~', a, '|', b, '&', a, '|', '~', b])

    def _remove_implies(self):
        match = re.search(r'(.*)->(.*)', self.cnf_formula)
        if match:
            antecedent, consequent = match.groups()
            self.cnf_equiv = self.cnf_formula
            self.cnf_formula = ''.join(['~', antecedent, '|', consequent])

    @staticmethod
    def _to_cnf(formula):
        # Remove whitespace characters
        formula = re.sub(r'\s+', '', formula)
        # Find clauses in CNF
        clauses = formula.split('&')

        need_adjust = [idx for idx, cl in enumerate(clauses) if len(cl) > 2 and (cl[0] == '~' and cl[1] == '(')]

        for f in need_adjust:
            defective_formula = clauses[f]
            if defective_formula.startswith('~'):
                # Destributive Negation
                defective_formula = defective_formula[1:]
                formula_parts = [s for s in defective_formula]
                i = 0
                while i < len(formula_parts):
                    # if formula_parts[i] == '(':
                    #     i += 1
                    if formula_parts[i] == '~':
                        # formula_parts[i] = formula_parts[i+1]
                        del formula_parts[i]
                        # i += 1
                    elif formula_parts[i] == '|':
                        formula_parts[i] = '&'
                        # i += 1
                    elif formula_parts[i] == '&':
                        formula_parts[i] = '|'
                        # i += 1
                    elif formula_parts[i] == ')':
                        break
                    i += 1

            res = ''.join(formula_parts)
            clauses[f] = res

    @staticmethod
    def _is_cnf(formula):
        # Remove whitespace characters
        formula = re.sub(r'\s+', '', formula)
        # Find clauses in CNF
        clauses = formula.split('&')
        # Test each clause for CNF pattern
        # ev = [len(cl) > 2 and ((cl[0] == '~' and cl[1] == '(') or not re.search(r'\|', cl)) for cl in clauses])
        # nev = not ev
        return all(
            [not (len(cl) > 2 and ((cl[0] == '~' and cl[1] == '(') or not re.search(r'\|', cl))) for cl in clauses])

    def _make_literals(self):
        self.literals = sorted(list(set([token[0] for token in self.tokens if token[1] == 'LITERAL'])))

    def _fix_negative_order(self, input_order):
        fix_order = input_order

        while fix_order:
            p = fix_order[0]

            if self.tokens[p + 1][1] == 'LPAREN':
                actual_pos = input_order.index(p)
                input_order[actual_pos], input_order[-1] = input_order[-1], input_order[actual_pos]

            fix_order = fix_order[1:]

    def _make_clauses(self):
        self.clauses = [x for x in self.literals]
        neg_positions = [pos for pos, lit in enumerate(self.tokens) if lit[1] == 'NOT']
        l_par = [pos for pos, lit in enumerate(self.tokens) if lit[1] == 'LPAREN']
        r_par = [pos for pos, lit in enumerate(self.tokens) if lit[1] == 'RPAREN']
        parens_positions = [(x, y) for x, y in zip(l_par, r_par)]

        self._fix_negative_order(neg_positions)

        start_parens = math.inf

        for idx, p in enumerate(neg_positions):
            if self.tokens[p + 1][1] != 'LPAREN':
                neg_cl = '~' + self.tokens[p + 1][0]
                if neg_cl not in self.clauses:
                    self.clauses.append(neg_cl)
            else:
                p_start, p_end = [c for c in parens_positions if c[0] == p + 1].pop()
                clause_at_p = ''.join([x[0] for x in self.tokens[p:p_end + 1]])
                start_parens = min(start_parens, len(self.clauses))
                self.clauses.append(clause_at_p)

        start_parens = min(start_parens, len(self.clauses))
        for p in parens_positions:
            res = [t[0] for idx, t in enumerate(self.tokens) if idx in range(p[0], p[1] + 1)]
            cl_parens = ''.join(res)
            if cl_parens not in self.clauses:
                self.clauses.insert(start_parens, cl_parens)
            start_parens += 1

    def _make_clause_token(self, clause: str) -> Tuple[str, str]:
        for regex, token_type in self.token_regexes:
            pattern = re.compile(regex)
            match = pattern.match(clause)
            if match:
                value = match.group(0)
                return value, token_type
        if not match:
            raise ValueError('Invalid token: ' + clause)

    def _fill_table_literals(self):
        rows = list(itertools.product([True, False], repeat=len(self.literals)))

        for i, l in enumerate(self.literals):
            self.truth_values[l] = [r[i] for r in rows]

    def _eval_clause(self, clause: str) -> List[bool]:
        reg_clauses = r'\(?(\~?\w+)\s?[\&|\|]\s?(\~?\w+)\)?'

        clause_arity = re.findall(reg_clauses, clause)

        if len(clause_arity) == 0:
            return self._eval_unary(clause)
        elif len(clause_arity) == 1 and isinstance(clause_arity[0], tuple):
            return self._eval_binary(clause, list(clause_arity[0]))

    def _eval_unary(self, literal: str) -> List[bool]:
        literals, cl = self._parse_clause(literal)

        if isinstance(cl[0], str) and str.lower(cl[0]) in ['not', '~']:
            return [not x for x in self.truth_values[cl[1]]]
        elif isinstance(cl[0], str):
            return [x for x in self.truth_values[cl[0]]]

    def _eval_binary(self, clause: str, literals: List[str]) -> List[bool]:
        results = {}
        for lit in literals:
            results[lit] = self._eval_unary(lit)

        if re.search(r'&', clause):
            # Conjunction Clause
            return [A and B for A, B in zip(results[literals[0]], results[literals[1]])]
        elif re.search(r'\|', clause):
            # Disjunction Clause
            return [A or B for A, B in zip(results[literals[0]], results[literals[1]])]

    @staticmethod
    def _parse_clause(formula):
        """Parses a boolean formula from string input."""
        formula = formula.replace("(", " ( ").replace(")", " ) ")
        # tokens = formula.split('')
        tokens = [s for s in formula if s != ' ']
        stack = [[]]
        variables = [v for v in tokens if v not in ['(', ')', 'AND', 'OR', 'NOT', '&', '|', '~']]
        for token in tokens:
            if token == "(":
                stack.append([])
            elif token == ")":
                inner = stack.pop()
                stack[-1].append(inner)
            else:
                stack[-1].append(token)
        return variables, stack[0]
