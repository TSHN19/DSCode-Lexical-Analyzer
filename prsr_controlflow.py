from prsr_errors import error_missing_semicolon
from prsr_arraypop import pop_first_element
from prsr_expressions import parse_expression
from prsr_statements import parse_statement

def parse_controlflow(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "break":
        return
    
    elif lexemes[0] == "continue":
        return
    
    elif lexemes[0] == "do":
        return
    
    elif lexemes[0] == "else":
        return
     
    elif lexemes[0] == "for":
        for_line_value = pop_first_element(number_line, tokens, lexemes)

        if tokens[0] == "LPAREN":
            lparen_line_value = pop_first_element(number_line, tokens, lexemes)
            initialization = parse_statement(number_line, tokens, lexemes, lines, result, Node)

            if tokens[0] == "SEMICOLON":
                semicolon_line_value = pop_first_element(number_line, tokens, lexemes)
                condition = parse_expression(number_line, tokens, lexemes, lines, result, Node)

                if tokens[0] == "SEMICOLON":
                    semicolon2_line_value = pop_first_element(number_line, tokens, lexemes)
                    increment = parse_expression(number_line, tokens, lexemes, lines, result, Node)

                    if tokens[0] == "RPAREN":
                        pop_first_element(number_line, tokens, lexemes)
                        body = parse_statement(number_line, tokens, lexemes, lines, result, Node)
                        return Node("ForLoop", [initialization, condition, increment, body])
                    else:
                        lines.append(semicolon2_line_value)
                        result.append("Expected ')' after '(' in expression")

                else:
                    error_missing_semicolon(lines, semicolon_line_value, result, "initialization")
            else:
                error_missing_semicolon(lines, lparen_line_value, result, "initialization")
            
        else:
            lines.append(for_line_value)
            result.append("Invalid for loop syntax")
    
    elif lexemes[0] == "goto":
        return
    
    elif lexemes[0] == "if":
        return
    
    elif lexemes[0] == "return":
        return
    
    elif lexemes[0] == "switch":
        return
    
    elif lexemes[0] == "while":
        number_line_value = pop_first_element(number_line, tokens, lexemes)

        if tokens[0] == "LPAREN":
            lparen_line_value = pop_first_element(number_line, tokens, lexemes)
            condition = parse_expression(number_line, tokens, lexemes, lines, result, Node, Node)
            
            if tokens[0] == "RPAREN":
                pop_first_element(number_line, tokens, lexemes)
                body = parse_statement(number_line, tokens, lexemes, lines, result, Node)
                return Node("WhileLoop", [condition, body])

            else:
                lines.append(lparen_line_value)
                result.append("Expected ')' after '(' in expression")
                
        else:
            lines.append(number_line_value)
            result.append("Invalid for while loop syntax")