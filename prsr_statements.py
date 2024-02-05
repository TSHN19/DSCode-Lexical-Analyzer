from prsr_arraypop import pop_first_element
from prsr_errors import error_expected_after
from prsr_assignments import parse_assignment
from prsr_declaration import parse_declaration
from prsr_controlflow import parse_controlflow
from prsr_otherkeywords import parse_otherkeywords
from prsr_expressions import parse_expression

def parse_statement(number_line, tokens, lexemes, lines, result, Node):
    
    if tokens and tokens[0] == "LBRACE":
        popped_lbrace = pop_first_element(number_line, tokens, lexemes)

        # Statements Nodes

        if tokens and tokens[0] == "RBRACE":
            pop_first_element(number_line, tokens, lexemes)
            #return Node
        
        else:
            error_expected_after(lines, popped_lbrace[1], result, "')'", "'(' in expression")
