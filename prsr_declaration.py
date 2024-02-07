from prsr_errors import error_missing_semicolon, error_expected_after, error_invalid_syntax
from prsr_otherfunctions import pop_first_element
from prsr_expressions import parse_expression

assignment_operators = {
    "ASGN_OP", "ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP", "BTWANDASGN_OP", 
    "BTWORASGN_OP", "BTWXORASGN_OP", "RSHIFTASGN_OP", "LSHIFTASGN_OP", "INTRSCT_OP", "UNT_OP"}

# Check declaration grammar
def parse_declaration(number_line, tokens, lexemes, lines, result, Node):
    # Stores data type token[0] and number line[1] to popped_datatype
    popped_datatype = pop_first_element(number_line, tokens, lexemes)       
    
    # If data type is followed by an identifier
    if tokens and tokens[0] == "IDENTIFIER":
        # Stores identifier token[0] and number line[1] to popped_identifier
        popped_identifier = pop_first_element(number_line, tokens, lexemes)

        # If identifer is followed by comma, multiple declaration
        if tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
            multichild_node, lines, result = parse_multidec(popped_identifier, number_line, tokens, lexemes, lines, result, Node)
            node = Node("Declaration", [popped_datatype[0], multichild_node])
            return node, lines, result
        
        # If assignment
        elif tokens and tokens[0] in assignment_operators:
            node, lines, result = parse_assignment(popped_identifier, number_line, tokens, lexemes, lines, result, Node)
            return node, lines, result
        
        # If identifier is followed by a semicolon
        elif tokens and tokens[0] == "SEMICOLON":
            node = Node("Declaration", [popped_identifier[0]])
            pop_first_element(number_line, tokens, lexemes)
            return node, lines, result
        
        # Error if declaration is missing semicolon
        else:
            node = None
            error_missing_semicolon(lines, popped_identifier[1], result, "declaration")
            return node, lines, result

    # Error if data type is not followed by an identifier
    else:
        node = None
        error_expected_after(lines, popped_datatype[1], result, "Identifier", "DataType")
        return node, lines, result

def parse_multidec(popped_identifier, number_line, tokens, lexemes, lines, result, Node):
    nodes = [popped_identifier]

    if tokens and tokens[0] == "IDENTIFIER":
        while tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            nodes.append(popped_identifier)

            # Check if the identifier is followed by an assignment operator
            if tokens and tokens[0] in assignment_operators:
                popped_operator = pop_first_element(number_line, tokens, lexemes)
                expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
                nodes.append(Node("Assignment", [popped_identifier, popped_operator, expression]))

            # Check if there is another identifier after comma
            if tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
            else:
                break

        # If the last identifier is followed by a semicolon
        if tokens and tokens[0] == "SEMICOLON":
            pop_first_element(number_line, tokens, lexemes)
            # Include the current identifiers and their assignments in the Node
            node = [Node("DecNodes", [id]) for id in nodes]
            return node, lines, result
        
        else:
            node = None
            error_missing_semicolon(lines, popped_identifier[1], result, "declaration")
            return node, lines, result
    else:
        node = None
        error_expected_after(lines, popped_identifier[1], result, "Identifier", ",")
        return node, lines, result

def parse_assignment(poppedidentifier, number_line, tokens, lexemes, lines, result, Node):
    assignments = []
    popped_identifier = poppedidentifier

    while ((tokens and tokens[0] in assignment_operators) or (tokens and tokens[0] == "IDENTIFIER")):
        # Check if the identifier is followed by an assignment operator
        if tokens and tokens[0] in assignment_operators:
            popped_operator = pop_first_element(number_line, tokens, lexemes)
            expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
            assignments.append(Node("Assignment", [popped_identifier, popped_operator, expression]))

            if tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
            else:
                continue
        elif tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            if tokens and tokens[0] in assignment_operators:
                continue
            elif tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
                assignments.append(Node("DecNodes", [popped_identifier]))
        else:
            # Error: Expected assignment operator after identifier
            error_expected_after(lines, popped_identifier[1], result, "'='", "identifier in assignment")
            break

    # If expression is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = [Node("Assignment", [id]) for id in assignments]
        pop_first_element(number_line, tokens, lexemes)
        return node, lines, result

    # Error if assignment is missing semicolon
    else:
        node = None
        error_missing_semicolon(lines, popped_operator[1], result, "assignment")
        return node, lines, result

