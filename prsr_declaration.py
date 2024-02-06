from prsr_errors import error_missing_semicolon, error_expected_after
from prsr_otherfunctions import pop_first_element

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
            node = parse_multidec(number_line, tokens, lexemes, lines, result)
            return node, lines, result

        # If identifier is followed by a semicolon
        elif tokens and tokens[0] == "SEMICOLON":
            node = Node("Declaration", [popped_identifier[0]])
            pop_first_element(number_line, tokens, lexemes)
            return node, lines, result
        
        # Error if declaration is missing semicolon
        else:
            node = Node("", [])
            error_missing_semicolon(lines, popped_identifier[1], result, "declaration")
            return node, lines, result

    # Error if data type is not followed by an identifier
    else:
        pop_first_element(number_line, tokens, lexemes)
        node = Node("", [])
        error_expected_after(lines, popped_datatype[1], result, "Identifier", "DataType")
        return node, lines, result

def parse_multidec(number_line, tokens, lexemes, lines, result):
    return
