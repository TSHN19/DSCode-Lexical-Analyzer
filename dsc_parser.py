from prsr_otherfunctions import pop_first_element
from prsr_declaration import parse_declaration
from prsr_controlflow import parse_controlflow
from prsr_otherkeywords import parse_otherkeywords
from prsr_assignments import parse_assignment

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def  __repr__(self):
        return f"Node({self.value} : {self.children})"

def syntax_analyzer(number_line, tokens, lexemes):
    parser_result = []
    parser_lines = []
    statements = []
    number_line_copy = number_line
    tokens_copy = tokens
    lexemes_copy = lexemes

    # Iterate through each tokens
    while tokens_copy:
        print("Iterating")

        if "ERROR" in tokens_copy[0]:
            popped_values = pop_first_element(number_line_copy, tokens_copy, lexemes_copy)
            parser_lines.append(popped_values[1])
            parser_result.append("Invalid Token")
        
        elif tokens_copy[0] == "DATATYPE_KW":
            declaration = parse_declaration(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node)
            statements.append(declaration[0])
            parser_lines = declaration[1]
            parser_result = declaration[2]
            print(statements)
            
        elif tokens_copy[0] == "CTRLFLOW_KW":
            statements.append(parse_controlflow(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node))

        elif tokens_copy[0] == "KEYWORD":
            statements.append(parse_otherkeywords(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node))
        
        elif tokens_copy[0] == "IDENTIFIER":
            assignment = parse_assignment(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node)
            statements.append(assignment[0])
            parser_lines = assignment[1]
            parser_result = assignment[2]

        else:
            popped_values = pop_first_element(number_line_copy, tokens_copy, lexemes_copy)
            parser_lines.append(popped_values[1])
            parser_result.append("SYNTAX ERROR")

    if statements is True:
        return parser_lines, statements
    else:
        return parser_lines, parser_result
