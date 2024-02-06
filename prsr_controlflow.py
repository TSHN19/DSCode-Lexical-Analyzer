from prsr_errors import error_missing_semicolon, error_invalid_syntax, error_expected_after
from prsr_otherfunctions import pop_first_element
from prsr_expressions import parse_boolexpression
from prsr_statements import parse_statements
from prsr_assignments import parse_assignment

def parse_controlflow(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "break":
        return
    
    elif lexemes[0] == "continue":
        return
    
    elif lexemes[0] == "do":
        return do_while_loop(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "else":
        return
     
    elif lexemes[0] == "for":
        return for_loop(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "goto":
        return
    
    elif lexemes[0] == "if":
        return
    
    elif lexemes[0] == "return":
        return
    
    elif lexemes[0] == "switch":
        return
    
    elif lexemes[0] == "while":
        return while_loop(number_line, tokens, lexemes, lines, result, Node)


def while_condition(number_line, tokens, lexemes, lines, result, Node):
    popped_while = pop_first_element(number_line, tokens, lexemes)

    # If while is followed by a left parenthesis
    if tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

        # Check if while loop has a condition and followed by a right parenthesis
        if condition[0] and (tokens[0] == "RPAREN"):
            popped_rparen = pop_first_element(number_line, tokens, lexemes)
            node = Node("While", [condition[0]])
            pop_first_element(number_line, tokens, lexemes)
            return node, lines, result, popped_rparen[1]
              
        # Error if while condition not closed
        else:
            error_expected_after(lines, popped_lparen[1], result, ")", "while condition")

    # Error if no left parenthesis after while keyword
    else:
        error_expected_after(lines, popped_while[1], result, "'('", " while keyword")

def do_while_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_do = pop_first_element(number_line, tokens, lexemes)
    statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

    # Check do keyword is followed by statements
    if statements[0]:

        # If statements is followed by the while keyword
        if lexemes[0] == "while":
            condition = while_condition(number_line, tokens, lexemes, lines, result, Node)

            # If identifier is followed by a semicolon
            if tokens and tokens[0] == "SEMICOLON":
                node = Node("Do-WhileLoop", [Node("Do", [statements[0]]), condition[0]])
                pop_first_element(number_line, tokens, lexemes)
                return node, lines, result
                    
            # Error if declaration is missing semicolon
            else:
                error_missing_semicolon(lines, condition[3], result, "do-while loop")
        
        # Error if not followed by a while condition
        else:
            error_expected_after(lines, statements[1], result, "while", "'}' in the statement")
    
    # Error if invalid syntax for do-while loop
    else:
        error_invalid_syntax(lines, popped_do[1], result, "Do-While Loop")
    
    node = Node("", [])
    return node, lines, result

def while_loop(number_line, tokens, lexemes, lines, result, Node):
    condition = while_condition(number_line, tokens, lexemes, lines, result, Node)

    # Check if while keyword is followed by a condition
    if condition[0]:
        statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)
        node = Node("WhileLoop", [condition[0], statements[0]])
        pop_first_element(number_line, tokens, lexemes)
        return node, lines, result

    # Error if invalid syntax for for loop        
    else:
        error_invalid_syntax(lines, condition[3], result, "While Loop")

def for_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_for = pop_first_element(number_line, tokens, lexemes)
    
    if tokens and (tokens[0] == "LPAREN"):
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        initialization = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

        if tokens and initialization[0]:
            if tokens and (tokens[0] == "SEMICOLON"):
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                if tokens and condition[0]:
                    if tokens and (tokens[0] == "SEMICOLON"):
                        popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                        increment = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                        if tokens and increment[0]:
                            if tokens and (tokens[0] == "RPAREN"):
                                statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)
                                pop_first_element(number_line, tokens, lexemes)
                                return Node("ForLoop", [initialization, condition, increment, statements])
                            
                            else:
                                node = Node("", [])
                                error_expected_after(lines, increment[1], result, "')'", "update")
                                return node, lines, result
                            
                        else:
                            node = Node("", [])
                            error_expected_after(lines, popped_semicolon[1], result, "update", "';'")
                            return node, lines, result

                    else:
                        node = Node("", [])
                        error_missing_semicolon(lines, condition[1], result, "initialization")
                        return node, lines, result
                
                else:
                    node = Node("", [])
                    error_expected_after(lines, popped_semicolon[1], result, "condition", "';'")
                    return node, lines, result

            else:
                node = Node("", [])
                error_missing_semicolon(lines, initialization[1], result, "initialization")
        
        else:
            node = Node("", [])
            error_expected_after(lines, popped_lparen[1], result, "initialization", "'('")
            return node, lines, result
    
    else:
        node = Node("", [])
        error_invalid_syntax(lines, popped_for[1], result, "For Loop")
        return node, lines, result
