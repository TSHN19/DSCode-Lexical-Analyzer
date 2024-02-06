from prsr_errors import error_missing_semicolon, error_invalid_syntax, error_expected_after
from prsr_otherfunctions import pop_first_element
from prsr_expressions import parse_boolexpression
from prsr_statements import parse_statements

def parse_controlflow(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "break":
        return
    
    elif lexemes[0] == "continue":
        return
    
    elif lexemes[0] == "do":
        do_while_loop(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "else":
        return
     
    elif lexemes[0] == "for":
        for_line_value = pop_first_element(number_line, tokens, lexemes)

        if tokens[0] == "LPAREN":
            lparen_line_value = pop_first_element(number_line, tokens, lexemes)
            initialization = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            if tokens[0] == "SEMICOLON":
                semicolon_line_value = pop_first_element(number_line, tokens, lexemes)
                condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                if tokens[0] == "SEMICOLON":
                    semicolon2_line_value = pop_first_element(number_line, tokens, lexemes)
                    increment = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                    if tokens[0] == "RPAREN":
                        pop_first_element(number_line, tokens, lexemes)
                        body = parse_statements(number_line, tokens, lexemes, lines, result, Node)
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
            condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)
            
            if tokens[0] == "RPAREN":
                pop_first_element(number_line, tokens, lexemes)
                body = parse_statements(number_line, tokens, lexemes, lines, result, Node)
                return Node("WhileLoop", [condition, body])

            else:
                lines.append(lparen_line_value)
                result.append("Expected ')' after '(' in expression")
                
        else:
            lines.append(number_line_value)
            result.append("Invalid for while loop syntax")

def do_while_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_do = pop_first_element(number_line, tokens, lexemes)
    statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

    # Check do keyword is followed by statements
    if statements[0]:

        # If statements is followed by the while keyword
        if lexemes[0] == "while":
            popped_while = pop_first_element(number_line, tokens, lexemes)

            # If while is followed by a left parenthesis
            if tokens[0] == "LPAREN":
                popped_lparen = pop_first_element(number_line, tokens, lexemes)
                condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                # Check if while loop has a condition and followed by a right parenthesis
                if condition[0] and (tokens[0] == "RPAREN"):
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)
                    
                    # If identifier is followed by a semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Do-While Loop", [Node("Do", [statements]), Node("While", [condition])])
                        pop_first_element(number_line, tokens, lexemes)
                        return node, lines, result
                    
                    # Error if declaration is missing semicolon
                    else:
                        error_missing_semicolon(lines, popped_rparen[1], result, "do-while loop")
                
                # Error if while condition not closed
                else:
                    error_expected_after(lines, popped_lparen[1], result, ")", "while condition")

            # Error if no left parenthesis after while keyword
            else:
                error_expected_after(lines, popped_while[1], result, "'('", " while keyword")
        
        # Error if not followed by a while condition
        else:
            error_expected_after(lines, statements[1], result, "while", "'}' in the statement")
    
    # Error if invalid syntax for do-while
    else:
        error_invalid_syntax(lines, popped_do[1], result, "Do-While Loop")
    
    node = Node("", [])
    return node, lines, result
