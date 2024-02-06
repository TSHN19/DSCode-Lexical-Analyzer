from prsr_errors import error_missing_semicolon
from prsr_otherfunctions import pop_first_element
from prsr_errors import error_expected_after
from prsr_expressions import parse_boolexpression

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
        expression = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)
    
        # If expression is followed by semicolon
        if tokens and tokens[0] == "SEMICOLON":
            node = Node("Assignment", [popped_identifier[0], expression])
            pop_first_element(number_line, tokens, lexemes)
            return node, lines, result
        
        # Error if assignment is missing semicolon
        else:
            node = Node("", [])
            error_missing_semicolon(lines, popped_operator[1], result, "assignment")
            return node, lines, result
    
    # Error if identifier is not followed by an assignment operator
    else:
        node = Node("", [])
        error_expected_after(lines, popped_identifier[1], result, "'='", "identifier in assignment")
        return node, lines, result
