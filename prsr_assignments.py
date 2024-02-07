from prsr_errors import error_missing, error_invalid_syntax, error_missing_semicolon
from prsr_otherfunctions import pop_first_element
from prsr_errors import error_expected_after
from prsr_expressions import parse_expression

assignment_operators = {
    "ASGN_OP", "ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP", "BTWANDASGN_OP", 
    "BTWORASGN_OP", "BTWXORASGN_OP", "RSHIFTASGN_OP", "LSHIFTASGN_OP", "INTRSCT_OP", "UNT_OP"}

# Assignment, Addition, Subtraction, Multiplication, Division, Modulo, Bitwise (AND, OR, XOR), Right and Left Shift Assignment
def parse_assignment(number_line, tokens, lexemes, lines, result, Node):
    # Stores identifier token[0] and number line[1] to popped_identifier
    popped_identifier = pop_first_element(number_line, tokens, lexemes)

    # If identifier is followed by an assignment operator
    if tokens and tokens[0] in assignment_operators:
        popped_operator = pop_first_element(number_line, tokens, lexemes)

        if tokens:

            if tokens[0] in ("INT_CONST", "FLOAT_CONST", "IDENTIFIER"):
                expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
                node = Node("Assignment", [popped_identifier[0], expression])
                return node, lines, result
            
            else:
                node = None
                error_expected_after(lines, popped_operator[1], result, "identifier or constant", "assignment operator")
                return node, lines, result   

        else:
            node = None
            error_missing(lines, popped_operator[1], result, "assignment right hand side")
            return node, lines, result
    
    # Error if identifier is not followed by an assignment operator
    else:
        node = None
        error_expected_after(lines, popped_identifier[1], result, "an assignment operator", "identifier")
        return node, lines, result

def parse_assignment_statement(number_line, tokens, lexemes, lines, result, Node):
    assignment_statement = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

    if tokens:
        if tokens[0] == "SEMICOLON":
            return assignment_statement
    
        else:
            node = None
            error_missing_semicolon(lines, assignment_statement[1], result, "assignment expression")
            return node, lines, result
    else:
        node = None
        error_invalid_syntax(lines, assignment_statement[1][0], result, "Assignment")
        return node, lines, result   