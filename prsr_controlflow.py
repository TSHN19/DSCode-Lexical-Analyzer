from prsr_errors import error_missing, error_missing_semicolon, error_invalid_syntax, error_expected_after, error_invalid
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
        return if_statement(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "return":
        return
    
    elif lexemes[0] == "switch":
        return
    
    elif lexemes[0] == "while":
        return while_loop(number_line, tokens, lexemes, lines, result, Node)

def condition(number_line, tokens, lexemes, lines, result, Node):
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
                condition = condition(number_line, tokens, lexemes, lines, result, Node)

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
            return node, lines, result
        
    # Error if invalid syntax for do-while loop
    else:
        node = None
        error_expected_after(lines, popped_do[1], result, "{", "do keyword")
        return node, lines, result

def while_loop(number_line, tokens, lexemes, lines, result, Node):
    condition = condition(number_line, tokens, lexemes, lines, result, Node)
    
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

def for_update(number_line, tokens, lexemes, lines, result, Node):
    update_assignment = {"ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP"}
    update_increment = {"INCR_OP", "DECR_OP"}
    
    if tokens[0] == "IDENTIFIER":
        if tokens[1] in update_increment:
            popped_token = pop_first_element(number_line, tokens, lexemes)
            popped_increment = pop_first_element(number_line, tokens, lexemes)
            node_token = Node(popped_token[0], [popped_token[2]])
            node_increment = Node(popped_increment[0], [popped_increment[2]])

            node = Node("Update", [node_token, node_increment])
            return node, popped_increment[1], result
        else:
            assignment = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

            if assignment[0] != None:
                if assignment[0].value in update_assignment:
                    node = Node("Update", [assignment[0]])
                    return node, assignment[1], result

                else:
                    node = None
                    error_invalid_syntax(lines, lines[-1], result, "update")
                    return node, lines, result
            else:
                node = None
                return node, lines, result

    else:
        node = None
        error_invalid_syntax(lines, lines[-1], result, "update")
        return node, lines, result

def for_condition(number_line, tokens, lexemes, lines, result, Node):
    condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

    if condition != None:
        if tokens and (tokens[0] == "SEMICOLON"):
            popped_semicolon = pop_first_element(number_line, tokens, lexemes)
            node = Node("Condition", [condition])
            return node, popped_semicolon[1], result

        else:
            node = None
            error_missing_semicolon(lines, condition[1], result, "condition")
            return node, lines, result
        
    else:
        node = None
        return node, lines, result

def for_initialization(number_line, tokens, lexemes, lines, result, Node):
    if tokens[0] == "DATATYPE_KW":
        initialization = parse_declaration(number_line, tokens, lexemes, lines, result, Node)
        
        if initialization[0] != None:
            node = Node("Initialization", [initialization[0]])
            return node, initialization[1], result
        
        else:
            node = None
            return node, lines, result
        
    elif len(tokens) == 1 or tokens[1] == "SEMICOLON":
        popped_identifier = pop_first_element(number_line, tokens, lexemes)
        initialization = Node(popped_identifier[0], [popped_identifier[2]]), popped_identifier[1], result
    else:
        initialization = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

    if initialization[0] != None:
        if tokens:
            if tokens[0] == "SEMICOLON":
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                node = Node("Initialization", [initialization[0]])
                return node, popped_semicolon[1], result

            else:
                node = None
                error_missing_semicolon(lines, initialization[1], result, "initialization")
                return node, lines, result
        else:
            node = None
            error_expected_after(lines, initialization[1], result, "';'", "initialization")
            return node, lines, result
        
    else:
        node = None
        return node, lines, result

def for_loopcontrol(number_line, tokens, lexemes, lines, result, Node):
    initialization = for_initialization(number_line, tokens, lexemes, lines, result, Node)

    if initialization[0] != None:
        if tokens:
            condition = for_condition(number_line, tokens, lexemes, lines, result, Node)

            if condition[0] != None:
                if tokens:
                    update = for_update(number_line, tokens, lexemes, lines, result, Node)

                    if update[0] != None:
                        node = Node("Loop Control", [initialization[0], condition[0], update[0]])
                        return node, update[1], result

                    else:
                        node = None
                        return node, lines, result

                else:
                    node = None
                    error_expected_after(lines, initialization[1], result, "update", "';'")
                    return node, lines, result

            else:
                node = None
                return node, lines, result
        
        else:
            node = None
            error_expected_after(lines, initialization[1], result, "condition", "';'")
            return node, lines, result
    else:
        node = None
        return node, lines, result

def for_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_for = pop_first_element(number_line, tokens, lexemes)
    
    if tokens:
        if tokens[0] == "LPAREN":
            popped_lparen = pop_first_element(number_line, tokens, lexemes)

            if tokens:
                loop_control = for_loopcontrol(number_line, tokens, lexemes, lines, result, Node)

                if loop_control[0] != None:

                    if tokens and (tokens[0] == "RPAREN"):
                        popped_rparen = pop_first_element(number_line, tokens, lexemes)
                        
                        if tokens:
                            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

                            if statements[0] != None:    
                                node = Node("ForLoop", [loop_control[0], statements[0]])
                                return node
                            
                            else:
                                node = None
                                return node, lines, result
                        else:
                            node = None
                            error_expected_after(lines, popped_rparen[1], result, "'{'", "keyword")
                            return node, lines, result
                                                            
                    else:
                        node = None
                        error_expected_after(lines, loop_control[1], result, "')'", "update")
                        return node, lines, result
                    
                else:
                    node = None
                    return node, lines, result

            else:
                node = None
                error_expected_after(lines, popped_lparen[1], result, "initialization", "for keyword")
                return node, lines, result

        else:
            node = None
            error_expected_after(lines, popped_lparen[1], result, "'('", "for keyword")
            return node, lines, result
        
    else:
        node = None
        error_expected_after(lines, popped_for[1], result, "'('", "for keyword")
        error_invalid_syntax(lines, popped_for[1], result, "For Loop")
        return node, lines, result

def if_statement(number_line, tokens, lexemes, lines, result, Node):
    condition = condition(number_line, tokens, lexemes, lines, result, Node)

    if condition[0] != None:
        if tokens:
            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            if statements[0] != None:
                if lexemes[0] == "else":
                    if tokens:
                        return
                    else:
                        node = None
                        error_expected_after(lines, condition[1], result, "condition", "if")
                        return node, lines, result
                else:
                    node = Node("IF", [condition[0], statements[0]])
                        
            else:
                node = None
                return node, lines, result

        else:
            node = None
            error_expected_after(lines, condition[1], result, "condition", "if")
            return node, lines, result

    else:
        node = None
        return node, lines, result
'''
def if_statements(number_line, tokens, lexemes, lines, result, Node):
    in_if_statement = 1

    while in_if_statement != 0:

                
            
            and tokens[0] == "LBRACE":
                
                if tokens and tokens[0] == "SEMICOLON":
                    pop_first_element(number_line, tokens, lexemes)
                    

                    if lexemes:
                        if lexemes[0] == "if":
                            in_if_statement = in_if_statement + 1
                            continue
                        elif lexemes[0] == "else":
                            else_condition = else_statements(number_line, tokens, lexemes, lines, result, Node, in_if_statement)
                            ifelse.append(else_condition[0])
                            in_if_statement = in_if_statement - 1 
                            continue
                        else:
                            node = [Node("Conditional", [id]) for id in ifelse]
                            return node, lines, result
                    else:
                        node = [Node("Conditional", [id]) for id in ifelse]
                        return node, lines, result
                else:
                    node = condition
                    error_missing_semicolon(lines, condition[3], result, "declaration")
                    return node, lines, result
                    
            # Error if condition is empty
            else:
                node = condition
                error_expected_after(lines, condition[3], result, "'{'", "declaration")
                return node, lines, result

        # Error if invalid syntax for while loop        
        else:
            node = None
            error_invalid_syntax(lines, condition[3], result, "If Statement")
            return node, lines, result'''

def else_statements(number_line, tokens, lexemes, lines, result, Node, in_if_statement):
    if in_if_statement != 0:
        if tokens:
            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            if statements[0] != None:
                return
            
            else:
                if lexemes[0] == "if":
                    popped_if = pop_first_element(number_line, tokens, lexemes)
                    else_if = if_statement(number_line, tokens, lexemes, lines, result, Node)

                else:
                    node = None
                    return node, lines, result

        else:
            node = None
            # error_expected_after(lines, value, result, "'{' or if", "else")
            return node, lines, result


        if condition[0] != None:
            if tokens and tokens[0] == "LBRACE":
                statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)
                if tokens and tokens[0] == "SEMICOLON":
                    pop_first_element(number_line, tokens, lexemes)
                    node = Node("Else", [condition[0], statements[0]])
                    return node, lines, result
                else:
                    node = condition
                    error_missing_semicolon(lines, condition[3], result, "declaration")
                    return node, lines, result
                    
            # Error if condition is empty
            else:
                node = condition
                error_expected_after(lines, condition[3], result, "'{'", "declaration")
                return node, lines, result

        # Error if invalid syntax for while loop        
        else:
            node = None
            error_invalid_syntax(lines, condition[3], result, "Else Statement")
            return node, lines, result
    else:
        node = None
        error_missing(lines, tokens, result, "IF statement")
        return node, lines, result

def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    if tokens and tokens[0] == "LBRACE":
        popped_lbrace = pop_first_element(number_line, tokens, lexemes)

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
        error_expected_after(lines, number_line[0], result, "'{'", "keyword")
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
