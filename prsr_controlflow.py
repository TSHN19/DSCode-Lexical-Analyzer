from prsr_errors import error_missing, error_missing_semicolon, error_invalid_syntax, error_expected_after, error_invalid
from prsr_otherfunctions import pop_first_element
from prsr_expressions import parse_boolexpression, parse_expression
from prsr_assignments import parse_assignment
from prsr_otherkeywords import parse_otherkeywords
from prsr_declaration import parse_declaration

def check_for_error(node, Node):
    if node.value == "Error":
        return True
    else:
        # If it's not an error or a leaf node, recursively check its children
        for child in node.children:
            if check_for_error(child, Node):
                return True
        return False

def parse_controlflow(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "break":
        return parse_break(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "continue":
        return parse_continue(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "do":
        return do_while_loop(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "else":
        return else_statement(number_line, tokens, lexemes, lines, result, Node)
     
    elif lexemes[0] == "for":
        return for_loop(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "goto":
        return parse_goto(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "if":
        return if_statement(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "return":
        return parse_return(number_line, tokens, lexemes, lines, result, Node)
    
    elif lexemes[0] == "while":
        return while_loop(number_line, tokens, lexemes, lines, result, Node)

# Break Statement
def parse_break(number_line, tokens, lexemes, lines, result, Node):
    popped_break = pop_first_element(number_line, tokens, lexemes)

    # Check if break is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
            node = Node("Break", [popped_break[2]])
            pop_first_element(number_line, tokens, lexemes)
            return node, popped_break[1], result

    # Error if missing semicolon
    else:
        node = Node("Break", [Node("Error", [])])
        error_missing_semicolon(lines, popped_break[1], result, "break")
        return node, popped_break[1], result

# Continue Statement
def parse_continue(number_line, tokens, lexemes, lines, result, Node):
    popped_continue = pop_first_element(number_line, tokens, lexemes)

    #Check if continue is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = Node("Continue", [popped_continue[0]])
        pop_first_element(number_line, tokens, lexemes)
        return node, popped_continue[1], result

    #Check if missing semicolon
    else:
        node = Node("Continue", [Node("Error", [])])
        error_missing_semicolon(lines, popped_continue[1], result, "continue")
        return node, popped_continue[1], result

# Return Statement
def parse_return(number_line, tokens, lexemes, lines, result, Node):
    popped_return = pop_first_element(number_line, tokens, lexemes)

    #Check if return is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = Node("Go-To", [popped_return[0]])
        pop_first_element(number_line, tokens, lexemes)
        return node, popped_return[1], result

    #Check if missing semicolon
    else:
        node = Node("Return", [Node("Error", [])])
        error_missing_semicolon(lines, popped_return[1], result, "return")
        return node, popped_return[1], result

# GoTo Statement
def parse_goto(number_line, tokens, lexemes, lines, result, Node):
    popped_goto = pop_first_element(number_line, tokens, lexemes)

    # Check if goto is followed by identifier
    if tokens and tokens[0] == "IDENTIFIER":
        popped_identifier = pop_first_element(number_line, tokens, lexemes)
        identifier = Node("Identifier", [popped_identifier[2]])

        #Check if identifier is followed by semicolon
        if tokens and tokens[0] == "SEMICOLON":
            node = Node("Go-To", [popped_identifier[0]])
            pop_first_element(number_line, tokens, lexemes)
            return node, popped_identifier[1], result

        #Check if missing semicolon
        else:
            node = Node("GoTo", [identifier, Node("Error", [])])
            error_missing_semicolon(lines, popped_identifier[1], result, "identifier")
            return node, popped_identifier[1], result
    
    # Error if missing identifier
    else:
        node = Node("GoTo", [Node("Error", [])])
        error_expected_after(lines, popped_goto[1], result, "identifier", "goto")
        return node, popped_goto[1], result

# Do-While, While, If, Else-If Condition
def condition(number_line, tokens, lexemes, lines, result, Node):
    popped_keyword = pop_first_element(number_line, tokens, lexemes)

    # If while is followed by a left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        
        # Check if tokens not empty
        if tokens:
            condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

            # Check if while loop has a condition
            if not check_for_error(condition[0], Node):

                # Check if condition is followed by a right parenthesis
                if tokens and tokens[0] == "RPAREN":
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)
                    node = Node("Condition", [condition[0]])
                    return node, popped_rparen[1], result

                # Error if while condition not closed
                else:
                    node = Node(popped_keyword[2].capitalize(), [condition[0], Node("Error", [])])
                    error_expected_after(lines, popped_lparen[1], result, "')'", " condition")
                    return node, condition[1], result
            
            # Error if invalid condition
            else:
                node = condition[0]
                popped_value = pop_first_element(number_line, tokens, lexemes)
                lines[-1] = popped_value[1]
                result[-1] = "Expected condition after '('"
                return node, condition[1], result
        
        # Error if missing condition
        else:
            node = Node(popped_keyword[2].capitalize(), [Node("Error", [])])
            error_expected_after(lines, popped_lparen[1], result, " condition", "'('")
            return node, popped_lparen[1], result

    # Error if no left parenthesis after while keyword
    else:
        node = Node(popped_keyword[2].capitalize(), [Node("Error", [])])
        error_expected_after(lines, popped_keyword[1], result, "'('", " keyword")
        return node, popped_keyword[1], result

def do_while_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_do = pop_first_element(number_line, tokens, lexemes)

    if tokens:
        statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

        # Check do keyword is followed by statements
        if statements[0] != None:

            # If statements is followed by the while keyword
            if tokens and lexemes[0] == "while":
                while_condition = condition(number_line, tokens, lexemes, lines, result, Node)

                if while_condition[0] != None:

                    # If identifier is followed by a semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Do-WhileLoop", [Node("Do", [statements[0]]), while_condition[0]])
                        pop_first_element(number_line, tokens, lexemes)
                        return node, lines, result
                            
                    # Error if declaration is missing semicolon
                    else:
                        node = None
                        error_missing_semicolon(lines, while_condition[1], result, "do-while loop")
                        return node, lines, result
                    
                else:
                    node = None
                    return node, lines, result
            
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

# While and Do-While Loop
def while_loop(number_line, tokens, lexemes, lines, result, Node):
    while_condition = condition(number_line, tokens, lexemes, lines, result, Node)
    
    # Check if while keyword is followed by a condition
    if not check_for_error(while_condition[0], Node):

        if tokens and tokens[0] == "LBRACE":
            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            # Check if condition is followed by statement
            if not check_for_error(statements[0], Node):
                node = Node(while_condition[0].value, [while_condition[0], statements[0]])
                return node, while_condition[1], result
            
            # Error if missing statements
            else:
                node = statements[0]
                return node, statements[1], result
        
        # Error if condition is empty
        else:
            node = Node(while_condition[0].value, [Node("Error", [])])
            error_expected_after(lines, while_condition[1], result, "'{'", "declaration")
            return node, while_condition[1], result

    # Error if invalid syntax for while loop        
    else:
        node = while_condition[0]
        return node, while_condition[1], result

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
                                return node, statements[1], result
                            
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
        return node, lines, result

def if_statement(number_line, tokens, lexemes, lines, result, Node):
    if_condition = condition(number_line, tokens, lexemes, lines, result, Node)

    if if_condition[0] != None:
        if tokens and tokens[0] == "LBRACE":
            statements = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            if statements[0] != None:
                if tokens and lexemes[0] == "else":
                    else_elseif = else_statement(number_line, tokens, lexemes, lines, result, Node)
                    
                    if else_elseif[0] != None:
                        node = Node("If-Else", [else_elseif[0]])
                        return node, statements[1], result
                    
                    else:
                        node = None
                        return node, lines, result

                else:
                    node = Node("If", [if_condition[0], statements[0]])
                    return node, lines, result
                        
            else:
                node = None
                return node, lines, result

        else:
            node = None
            error_expected_after(lines, if_condition[1], result, "'{'", "declaration")
            return node, lines, result

    else:
        node = None
        return node, lines, result
    
def else_statement(number_line, tokens, lexemes, lines, result, Node):
    popped_else = pop_first_element(number_line, tokens, lexemes)

    if tokens:
        if lexemes[0] == "if":
            statement = if_statement(number_line, tokens, lexemes, lines, result, Node)

            if statement[0] != None:
                node = Node("Else-If", [statement[0]])
                return node, lines, result

            else:
                node = None
                return node, lines, result

        elif tokens[0] == "LBRACE":
            statement = parse_statements(number_line, tokens, lexemes, lines, result, Node)

            if statement[0] != None:
                node = Node("Else", [statement[0]])
                return node, lines, result

            else:
                node = None
                return node, lines, result

        else:
            node = None
            error_expected_after(lines, popped_else[1], result, "if or '{'", "else")
            return node, lines, result
    else:
        node = None
        error_expected_after(lines, popped_else[1], result, "if or '{'", "else")
        return node, lines, result

def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    popped_lbrace = pop_first_element(number_line, tokens, lexemes)

    if tokens and tokens[0] == "RBRACE":
        popped_rbrace = pop_first_element(number_line, tokens, lexemes)
        node = Node("", []) # Add node
        return node, popped_rbrace[1], result
    
    else:
        node = None
        error_expected_after(lines, popped_lbrace[1], result, "'}'", "'{' in expression")
        return node, popped_lbrace[1], result
