from prsr_otherfunctions import pop_first_element
from prsr_errors import error_expected_after
from prsr_expressions import parse_expression
from prsr_controlflow import parse_controlflow
from prsr_otherkeywords import parse_otherkeywords
from prsr_declaration import parse_declaration
from prsr_assignments import parse_assignment


def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    
    if tokens and tokens[0] == "LBRACE":
        popped_lbrace = pop_first_element(number_line, tokens, lexemes)
        
        #Parsing various components of statement
        expression_node, lines, result = parse_expression(number_line, tokens, lexemes, lines, result)
        controlflow_node, lines, result = parse_controlflow(number_line, tokens, lexemes, lines, result)
        otherkeywords_node, lines, result = parse_otherkeywords(number_line, tokens, lexemes, lines, result)
        declaration_node, lines, result = parse_declaration(number_line, tokens, lexemes, lines, result)
        assignment_node, lines, result = parse_assignment(number_line, tokens, lexemes, lines, result)

        if tokens and tokens[0] == "RBRACE":
            pop_first_element(number_line, tokens, lexemes)
            
            #Creating a compound node with all parsed nodes
            node = Node("Statements", [expression_node, controlflow_node, otherkeywords_node, declaration_node, assignment_node]) # Add node
            return node, lines, result
        
        else:

            #Creating a compound node with all parsed nodes
            node = Node("Statements", [expression_node, controlflow_node, otherkeywords_node, declaration_node, assignment_node])
            
            #Error Handling
            error_expected_after(lines, popped_lbrace[1], result, "'}'", "'{' in expression")
            return node, lines, result
        
