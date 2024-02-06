from prsr_otherfunctions import pop_first_element
from prsr_errors import error_expected_after

def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    
    if tokens and tokens[0] == "LBRACE":
        popped_lbrace = pop_first_element(number_line, tokens, lexemes)
        
        # Statements Nodes

        if tokens and tokens[0] == "RBRACE":
            pop_first_element(number_line, tokens, lexemes)
            node = Node("", []) # Add node
            return node, lines, result
        
        else:
            node = Node("", [])
            error_expected_after(lines, popped_lbrace[1], result, "'}'", "'{' in expression")
            return node, lines, result
