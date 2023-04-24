from boolean_formulas import EvalFormula


def test_cnf(formula_str):
    # Create EvalFormula instance
    my_formula = EvalFormula(formula_str)

    # Process Formula
    my_formula.tokenize()

    # Generate Truth Table
    my_formula.eval()

    print(f'Information about formula "{formula_str}":')

    # Get literals
    print(f'\t * contains {len(my_formula.literals)} literals: {my_formula.literals}')

    # Get truth table rows
    print(f'\t * has {my_formula.number_of_rows} rows')

    # Get truth table columns
    print(f'\t * contains {my_formula.number_of_columns} clauses: {my_formula.clauses}')

    # Show Generated truth table
    my_formula.print_table()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # formula = 'P | Q & R'
    # formula = 'p & (q | ~r)'
    # formula = 'p & (q | ~r) & ~(~s|t)'
    # formulas = ['D<->(C | E | ~F)', 'A->(B|~C)', '(P|Q)&R', 'p & (q | ~r)', 'p & (q | ~r) & ~(~s|t)']
    formulas = [
        # 'A->B',
        # '(A|B)->(C|D)',
        # '(A&B)->~C',
        # '~A|B',
        '(P|Q)&R',
        # 'p & (q | ~r)',
        # 'p & (q | ~r) & ~(~s|t)'
    ]
    for formula in formulas:
        test_cnf(formula)
