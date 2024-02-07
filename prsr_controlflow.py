from prsr_errors import error_expected, error_missing_semicolon, error_invalid_syntax, error_expected_after, error_missing
from prsr_otherfunctions import pop_first_element
from prsr_expressions import parse_boolexpression, parse_expression
from prsr_assignments import parse_assignment
from prsr_otherkeywords import parse_otherkeywords
from prsr_declaration import parse_declaration

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
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        
        if tokens:
            condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

            # Check if while loop has a condition
            if condition[0] != None:
                # Check if condition is followed by a right parenthesis
                if tokens and tokens[0] == "RPAREN":
                    pop_first_element(number_line, tokens, lexemes)
                    node = Node("Condition", [condition[0]])
                    return node, lines, result, popped_lparen[1]

                # Error if while condition not closed
                else:
                    node = None
                    error_expected_after(lines, popped_lparen[1], result, "')'", "while condition")
                    return node, lines, result, popped_lparen[1]
            
            else:
                node = None
                return node, lines, result, popped_lparen[1]
        
        else:
            node = None
            error_expected_after(lines, popped_lparen[1], result, "while condition", "'('")
            return node, lines, result, popped_lparen[1]

    # Error if no left parenthesis after while keyword
    else:
        node = None
        error_expected_after(lines, popped_while[1], result, "'('", " while keyword")
        return node, lines, result, popped_while[1]

def do_while_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_do = pop_first_element(number_line, tokens, lexemes)

    if tokens:
        statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

        # Check do keyword is followed by statements
        if statements[0] != None:

            # If statements is followed by the while keyword
            if tokens and lexemes[0] == "while":
                condition = while_condition(number_line, tokens, lexemes, lines, result, Node)

                if condition[0] != None:

                    # If identifier is followed by a semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Do-WhileLoop", [Node("Do", [statements[0]]), condition[0]])
                        pop_first_element(number_line, tokens, lexemes)
                        return node, lines, result
                            
                    # Error if declaration is missing semicolon
                    else:
                        node = None
                        error_missing_semicolon(lines, condition[3], result, "do-while loop")
                        return node, lines, result
                    
                else:
                    node = None
                    return node, lines, result, condition[3]
            
            # Error if not followed by a while condition
            else:
                node = None
                error_expected_after(lines, statements[1], result, "while", "'}' in the statement")
                return node, lines, result
            
        else:
            node = None
            error_expected_after(lines, popped_do[1], result, "statements", "do keyword")
            return node, lines, result
        
    # Error if invalid syntax for do-while loop
    else:
        node = None
        error_invalid_syntax(lines, popped_do[1], result, "Do-While Loop")
        return node, lines, result

def while_loop(number_line, tokens, lexemes, lines, result, Node):
    condition = while_condition(number_line, tokens, lexemes, lines, result, Node)
    
    # Check if while keyword is followed by a condition
    if condition[0] != None:
        if tokens and tokens[0] == "LBRACE":
            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)
            node = Node("WhileLoop", [condition[0], statements[0]])
            return node, lines, result
        
        # Error if condition is empty
        else:
            node = condition
            error_expected_after(lines, condition[3], result, "'{'", "declaration")
            return node, lines, result

    # Error if invalid syntax for while loop        
    else:
        node = None
        error_invalid_syntax(lines, condition[3], result, "While Loop")
        return node, lines, result

def for_condition1(number_line, tokens, lexemes, lines, result, Node):
    if tokens:
        condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

        if condition[0]:
            if tokens and (tokens[0] == "SEMICOLON"):
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)

                if tokens:
                    increment = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

                    if increment[0]:
                        return
                                            
                    else:
                        node = None
                        error_expected_after(lines, popped_semicolon[1], result, "update", "';'")
                        return node, lines, result
                                    
                else:
                    node = None
                    error_expected_after(lines, popped_semicolon[1], result, "update", "';'")
                    return node, lines, result

            else:
                node = None
                error_missing_semicolon(lines, condition[1], result, "initialization")
                return node, lines, result
        
        else:
            node = None
            error_expected_after(lines, popped_semicolon[1], result, "condition", "';'")
            return node, lines, result
    
    else:
        node = None
        error_expected_after(lines, popped_semicolon[1], result, "condition", "';'")
        return node, lines, result 

def for_update(number_line, tokens, lexemes, lines, result, Node):
    return

def for_condition(number_line, tokens, lexemes, lines, result, Node):
    return

def for_initialization(number_line, tokens, lexemes, lines, result, Node):
    initialization = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

    if initialization[0] != None:
        if tokens and (tokens[0] == "SEMICOLON"):
            pop_first_element(number_line, tokens, lexemes)
            return initialization

        else:
            node = None
            error_missing_semicolon(lines, initialization[1], result, "initialization")
            return node, lines, result
        
    else:
        node = None
        error_expected_after(lines, lines[-1], result, "assignment expression or identifier", "'('")
        return node, lines, result



def for_loopcontrol(number_line, tokens, lexemes, lines, result, Node):
    if tokens:
        return
    else:
        node = None
        error_expected_after(lines, lines[-1], result, "initialization", "'('")
        return node, lines, result


def for_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_for = pop_first_element(number_line, tokens, lexemes)
    
    if tokens:
        if tokens[0] == "LPAREN":
            popped_lparen = pop_first_element(number_line, tokens, lexemes)

            if tokens:
                loop_control = (number_line, tokens, lexemes, lines, result, Node)

                if loop_control[0] != None:

                    if tokens and (tokens[0] == "RPAREN"):
                        statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

                        if statements[0] != None:    
                            pop_first_element(number_line, tokens, lexemes)
                            return Node("ForLoop", [loop_control, statements])
                        
                        else:
                            node = None
                            error_expected_after(lines, loop_control[1], result, "statements", "loop control")
                            return node, lines, result
                                                            
                    else:
                        node = None
                        error_expected_after(lines, loop_control[1], result, "')'", "update")
                        return node, lines, result
                    
                else:
                    node = None
                    error_expected_after(lines, popped_lparen[1], result, "loop control", "for keyword")
                    return node, lines, result

            else:
                node = None
                return node, lines, result

        else:
            node = None
            error_expected_after(lines, popped_lparen[1], result, "'('", "for keyword")
            return node, lines, result
        
    else:
        node = None
        error_invalid_syntax(lines, popped_for[1], result, "For Loop")
        return node, lines, result

def if_condition(number_line, tokens, lexemes, lines, result, Node):
    return

def if_statements(number_line, tokens, lexemes, lines, result, Node):
    popped_if = pop_first_element(number_line, tokens, lexemes)
    statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

    # checks if the if statement is followed by left parentheses
    if tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

        # checks if the left parentheses is followed by a condition with a right parentheses
        if condition[0] and (tokens[0] == "RPAREN"):
            popped_rparen = pop_first_element(number_line, tokens, lexemes)

            # checks if condition is followed by a statement
            if statements[0]:

                if tokens and tokens[0] == "SEMICOLON":
                    node = Node("If Statement", [Node("If", [condition, statements])])
                    pop_first_element(number_line, tokens, lexemes)
                    return node, lines, result

                # error: missing semicolon
                else:
                    error_missing_semicolon(lines, popped_rparen[1], result, "if statement")

            # error: no statement after condition
            else:
                error_invalid_syntax(lines, popped_rparen[1], result, "if Statement")

        # error: expected right parentheses after condition
        else:
            error_expected_after(lines, popped_lparen[1], result, ")", "if condition")

    # Error if no left parenthesis after if keyword
    else:
        error_expected_after(lines, popped_if[1], result, "'('", " if keyword")

    node = Node("", [])
    return node, lines, result

def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    if tokens and tokens[0] == "LBRACE":
        popped_lbrace = pop_first_element(number_line, tokens, lexemes)
        
        # Statements Nodes

        if tokens and tokens[0] == "RBRACE":
            popped_rbrace = pop_first_element(number_line, tokens, lexemes)
            node = Node("", []) # Add node
            return node, popped_rbrace[1], result
        
        else:
            node = None
            error_expected_after(lines, popped_lbrace[1], result, "'}'", "'{' in expression")
            return node, lines, result
    else:
        node = None
        error_expected_after(lines, number_line[0], result, "'{'", "do keyword")
        return node, lines, result
    
    '''
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
    '''
