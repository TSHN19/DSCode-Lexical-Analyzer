from prsr_otherfunctions import pop_first_element
from prsr_errors import error_unexpected_tokens, error_invalid_syntax, error_expected, error_missing, error_expected_after, error_missing_semicolon

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def  __repr__(self):
        return f"Node({self.value} : {self.children})"

def syntax_analyzer(number_line, tokens, lexemes):
    
    parser_result = []
    parser_lines = []
    parser_nodes = []
    number_line_copy = number_line
    tokens_copy = tokens
    lexemes_copy = lexemes

    # Iterate through each tokens
    while tokens_copy:
        print("Iterating")

        if tokens and tokens[0] == "LBRACE":
            popped_lbrace = pop_first_element(number_line, tokens, lexemes)
            statement = parse_statements(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node)
            parser_nodes.append(statement[0])

        if "ERROR" in tokens_copy[0]:
            popped_values = pop_first_element(number_line_copy, tokens_copy, lexemes_copy)
            parser_lines.append(popped_values[1])
            parser_result.append("Invalid Token")
        
        elif tokens_copy[0] == "DATATYPE_KW":
            declaration = parse_declaration(number_line_copy, tokens_copy, lexemes_copy, parser_lines, parser_result, Node)
            parser_nodes.append(declaration[0])

        else:
            popped_values = pop_first_element(number_line_copy, tokens_copy, lexemes_copy)
            parser_lines.append(popped_values[1])
            parser_result.append("SYNTAX ERROR: '" + popped_values[2] + "'")
    
    
    return parser_lines, parser_result, parser_nodes

def parse_statements(number_line, tokens, lexemes, lines, result, Node):
    statements = []

    while tokens:
        if "ERROR" in tokens[0]:
            popped_values = pop_first_element(number_line, tokens, lexemes)
            node = None
            error_unexpected_tokens(lines, popped_values[1], result, "Error")
            return node, lines.append(popped_values[1]), result

        elif tokens and tokens[0] == "LBRACE":
            popped_lbrace = pop_first_element(number_line, tokens, lexemes)
            statement = parse_statements(number_line, tokens, lexemes,lines, result, Node)
            statements.append(statement[0])

            if tokens and tokens[0] == "RBRACE":
                popped_rbrace = pop_first_element(number_line, tokens, lexemes)
                
                #Creating a compound node with all parsed nodes
                node = [Node("Statements", [id]) for id in statements]
                return node, lines.append(popped_rbrace[1]), result
            else:
                statement.append(Node("Error", []))
                node = [Node("Statements", [id]) for id in statements]
                error_expected_after(lines, popped_lbrace[1], result, "'}'", "'{' in expression")
                return node, lines.append(popped_lbrace[1]), result

        elif tokens[0] == "DATATYPE_KW":
            declaration = parse_declaration(number_line, tokens, lexemes, lines, result, Node)
            statements.append(declaration[0])
            
        elif tokens[0] == "CTRLFLOW_KW":
            controlflow = parse_controlflow(number_line, tokens, lexemes, lines, result, Node)
            statements.append(controlflow[0])

        elif tokens[0] == "KEYWORD":
            keyword = parse_otherkeywords(number_line, tokens, lexemes, lines, result, Node)
            statements.append(keyword[0])

        elif tokens[0] == "IDENTIFIER":
            assignment = parse_assignment_statement(number_line, tokens, lexemes, lines, result, Node)
            statements.append(assignment[0])
        
        elif tokens and tokens[0] == "RBRACE":
            node = [Node("Statements", [id]) for id in statements]
            return node, lines, result

        else:
            popped_values = pop_first_element(number_line, tokens, lexemes)
            node = None
            error_invalid_syntax(lines, popped_values[1], result, "EWAN")
            return node, lines.append(popped_values[1]), result

"""
E X P R E S S I O N S   H A N D L I N G
Check expressions and operators used following their order of precedence
    1. PARENTHESIS
    2. UNARY OPERATORS: ++, --, !, ~
    3. MULTIPLICATIVE OPERATORS: *, /, %
    4. ADDITIVE OPERATORS: +, -, >|<, #&#
    5. SHIFT OPERATORS: <<, >>
    6. RELATIONAL OPERATORS: <, >, <=, >=, ??
    7. EQUALITY OPERATORS: !=, ==
    8. BITWISE AND OPERATOR: &
    9. BITWISE XOR OPERATOR: ^
    10.BITWISE OR OPERATOR: |
    11.LOGICAL AND OPERATOR: &&
    12.LOGICAL OR OPERATOR: ||
"""

boolean_operators = [
    "LOGOR_OP", "LOGAND_OP", "LSSTHN_OP", "GRTRTHN_OP", "LSSEQL_OP", 
    "GRTREQL_OP", "NOTEQLTO_OP", "EQLTO_OP"]

def parse_boolexpression(number_line, tokens, lexemes, lines, result, Node):
    is_expression = False
    node = parse_logical_or(number_line, tokens, lexemes, lines, result, Node, is_expression)

    if node[0] == None:
        return node[0], number_line, result

    node_line = node[1]

    check_node = node[0].value 
    check = check_node in boolean_operators
    
    if not check:
        # Handle the case where there is no boolean operator
        node = Node("Condition", [node[0], Node("Error", [])])
        error_expected(lines, node_line, result, "conditional expression")
        return node, node_line, result

    return node[0], node_line

def parse_expression(number_line, tokens, lexemes, lines, result, Node):
    is_expression = False
    node = parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node, is_expression = True)
    return node

# Logical OR Operator
def parse_logical_or(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_logical_and(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] == "LOGOR_OP":
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_logical_and(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Logical AND Operator
def parse_logical_and(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] == "LOGAND_OP":
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Bitwise OR Operator
def parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] == "BTWOR_OP":
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Bitwise XOR Operator
def parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] == "BTWXOR_OP":
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Bitwise AND Operator
def parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_equality(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] == "BTWAND_OP":
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_equality(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Not Equal To and Equal To Operators
def parse_equality(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_relational(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("NOTEQLTO_OP", "EQLTO_OP"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_relational(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Greater Than, Less Than, Greater Than or Equal To, and Less Than or Equal To Operators
def parse_relational(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_shift(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("GRTRTHN_OP", "LSSTHN_OP", "GRTREQL_OP", "LSSEQL_OP", "SRCH_OP"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_shift(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Right Shift and Left Shift Operators
def parse_shift(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_additive(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("RSHIFT_OP", "LSHIFT_OP"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_additive(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Plus and Minus Operators
def parse_additive(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_multiplicative(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("PLUS_OP", "MINUS_OP", "INTRSCT_OP", "UNT_OP" ):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_multiplicative(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Multiply, Divide, and Modulo Operators
def parse_multiplicative(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_unary(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("MULTIPLY_OP", "DIVIDE_OP", "MODULO_OP"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_unary(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line

    return node[0], line

# Increment, Decrement, Logical Not, and Bitwise Not Operators
def parse_unary(number_line, tokens, lexemes, lines, result, Node, is_expression):
    node = parse_factor(number_line, tokens, lexemes, lines, result, Node, is_expression)
    line = node[1]

    while tokens and tokens[0] in ("INCR_OP", "DECR_OP", "LOGNOT_OP", "BTWNOT_OP"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        right_node = parse_factor(number_line, tokens, lexemes, lines, result, Node, is_expression)
        node = Node(popped_values[0], [node[0], right_node[0]])
        return node, line
    
    return node[0], line

# Handle integer and float constants, identifiers, and parenthesis
def parse_factor(number_line, tokens, lexemes, lines, result, Node, is_expression):
    if tokens[0] in ("INT_CONST", "FLOAT_CONST", "IDENTIFIER"):
        popped_values = pop_first_element(number_line, tokens, lexemes)
        node = Node(popped_values[0], [popped_values[2]])
        return node, lines.append(popped_values[1])
    
    elif tokens[0] == "LPAREN":
        popped_values = pop_first_element(number_line, tokens, lexemes)

        if is_expression:
            expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
        else:
            bool_expression = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

        if tokens and tokens[0] == "RPAREN":
            pop_first_element(number_line, tokens, lexemes)
            expression if is_expression else bool_expression

        else:
            node = None
            error_expected_after(lines, popped_values[1], result, "')'", "'(' in expression")
            return node, lines, result
    
    else:
        node = None
        error_unexpected_tokens(lines, number_line[0], result, tokens[0])
        return node, lines, result, tokens[0]

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
        return node, lines.append(popped_break[1]), result

    # Error if missing semicolon
    else:
        node = Node("Break", [Node("Error", [])])
        error_missing_semicolon(lines, popped_break[1], result, "break")
        return node, lines.append(popped_break[1]), result

# Continue Statement
def parse_continue(number_line, tokens, lexemes, lines, result, Node):
    popped_continue = pop_first_element(number_line, tokens, lexemes)

    #Check if continue is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = Node("Continue", [popped_continue[2]])
        pop_first_element(number_line, tokens, lexemes)
        return node, lines.append(popped_continue[1]), result

    #Check if missing semicolon
    else:
        node = Node("Continue", [Node("Error", [])])
        error_missing_semicolon(lines, popped_continue[1], result, "continue")
        return node, lines.append(popped_continue[1]), result

# Return Statement
def parse_return(number_line, tokens, lexemes, lines, result, Node):
    popped_return = pop_first_element(number_line, tokens, lexemes)

    #Check if return is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = Node("Return", [popped_return[2]])
        pop_first_element(number_line, tokens, lexemes)
        return node, lines.append(popped_return[1]), result

    #Check if missing semicolon
    else:
        node = Node("Return", [Node("Error", [])])
        error_missing_semicolon(lines, popped_return[1], result, "return")
        return node, lines.append(popped_return[1]), result

# GoTo Statement
def parse_goto(number_line, tokens, lexemes, lines, result, Node):
    popped_goto = pop_first_element(number_line, tokens, lexemes)

    # Check if goto is followed by identifier
    if tokens and tokens[0] == "IDENTIFIER":
        popped_identifier = pop_first_element(number_line, tokens, lexemes)
        identifier = Node("Identifier", [popped_identifier[2]])

        #Check if identifier is followed by semicolon
        if tokens and tokens[0] == "SEMICOLON":
            node = Node("Go-To", [identifier])
            pop_first_element(number_line, tokens, lexemes)
            return node, lines.append(popped_identifier[1]), result

        #Check if missing semicolon
        else:
            node = Node("GoTo", [identifier, Node("Error", [])])
            error_missing_semicolon(lines, popped_identifier[1], result, "identifier")
            return node, lines.append(popped_identifier[1]), result
    
    # Error if missing identifier
    else:
        node = Node("GoTo", [Node("Error", [])])
        error_expected_after(lines, popped_goto[1], result, "identifier", "goto")
        return node, lines.append(popped_goto[1]), result

# Do-While, While, If, Else-If Condition
def condition(number_line, tokens, lexemes, lines, result, Node):
    popped_keyword = pop_first_element(number_line, tokens, lexemes)

    # If while is followed by a left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)

        # Check if tokens not empty
        if tokens:
            condition = parse_boolexpression(number_line, tokens, lexemes, lines, result, Node)

            # Check if error occured in condition
            if result:
                result[-1] = "Expected conditional expression after '('"

            # Check if condition is followed by a right parenthesis
            if tokens and tokens[0] == "RPAREN":
                popped_rparen = pop_first_element(number_line, tokens, lexemes)
                node = Node("Condition", [condition[0]])
                return node, lines.append(popped_rparen[1]), result

            # Error if while condition not closed
            else:
                node = Node(popped_keyword[2].capitalize(), [condition[0], Node("Error", [])])
                error_expected_after(lines, popped_lparen[1], result, "')'", " condition")
                return node, lines.append(condition[1]), result
              
        # Error if missing condition
        else:
            node = Node(popped_keyword[2].capitalize(), [Node("Error", [])])
            error_expected_after(lines, popped_lparen[1], result, " condition", "'('")
            return node, lines.append(popped_lparen[1]), result

    # Error if no left parenthesis after while keyword
    else:
        node = Node(popped_keyword[2].capitalize(), [Node("Error", [])])
        error_expected_after(lines, popped_keyword[1], result, "'('", " keyword")
        return node, lines.append(popped_keyword[1]), result

# Do-While Loop
def do_while_loop(number_line, tokens, lexemes, lines, result, Node):
    popped_do = pop_first_element(number_line, tokens, lexemes)

    # Check if tokens not empty
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
    
    # Check if condition is followed by left brace
    if tokens and tokens[0] == "LBRACE":
        node = while_condition[0]
        return node, lines.append(while_condition[1]), result, True        
        
    # Error if condition is empty
    else:
        node = Node(while_condition[0].value, [Node("Error", [])])
        error_expected_after(lines, while_condition[1], result, "'{'", "declaration")
        return node, lines.append(while_condition[1]), result

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
            return node, lines.append(popped_increment[1]), result
        else:
            assignment = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

            if assignment[0] != None:
                if assignment[0].value in update_assignment:
                    node = Node("Update", [assignment[0]])
                    return node, lines.append(assignment[1]), result

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
            return node, lines.append(popped_semicolon[1]), result

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
            return node, lines.append(initialization[1]), result
        
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
                return node, lines.append(popped_semicolon[1]), result

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
                        return node, lines.append(update[1]), result

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
                                return node, lines.append(statements[1]), result
                            
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
                        return node, lines.append(statements[1]), result
                    
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

# Assignment, Addition, Subtraction, Multiplication, Division, Modulo, Bitwise (AND, OR, XOR), Right and Left Shift Assignment
def parse_assignment(number_line, tokens, lexemes, lines, result, Node):
    assignment_operators = [
        "ASGN_OP", "ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP", "BTWANDASGN_OP", 
        "BTWORASGN_OP", "BTWXORASGN_OP", "RSHIFTASGN_OP", "LSHIFTASGN_OP", "INTRSCT_OP", "UNT_OP",
        "INSRT_OP", "RMV_OP", "RCSVDQ_OP", "PRTYEQ_OP"]
    
    # Stores identifier token[0] and number line[1] to popped_identifier
    popped_identifier = pop_first_element(number_line, tokens, lexemes)
    identifier = Node("Identifier", [popped_identifier[2]])

    # If identifier is followed by an assignment operator
    if tokens and tokens[0] in assignment_operators:
        popped_operator = pop_first_element(number_line, tokens, lexemes)
        operator = Node("AssignmentOperator", [popped_operator[2]])

        if tokens and tokens[0] in ("INT_CONST", "FLOAT_CONST", "IDENTIFIER"):
                expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
                node = Node("Assignment", [identifier, operator, expression[0]])
                return node, lines.append(popped_operator[1]), result

        else:
            node = Node("Assignment", [identifier, operator, Node("Error", [])])
            error_missing(lines, popped_operator[1], result, "assignment right hand side")
            return node, lines.append(popped_operator[1]), result
    
    # Error if identifier is not followed by an assignment operator
    else:
        node = Node("Assignment", [identifier, Node("Error", [])])
        error_expected_after(lines, popped_identifier[1], result, "an assignment operator", "identifier")
        return node, lines.append(popped_identifier[1]), result

def parse_assignment_statement(number_line, tokens, lexemes, lines, result, Node):
    assignment = parse_assignment(number_line, tokens, lexemes, lines, result, Node)

    if tokens and tokens[0] == "SEMICOLON":
            pop_first_element(number_line, tokens, lexemes)
            return assignment
    
    else:
        node = Node(assignment[0].value, [assignment[0], Node("Error", [])])
        error_expected_after(lines, assignment[1], result, "';'", "assignment expression")
        return node, lines, result   

assignment_operators = {
    "ASGN_OP", "ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP", "BTWANDASGN_OP", 
    "BTWORASGN_OP", "BTWXORASGN_OP", "RSHIFTASGN_OP", "LSHIFTASGN_OP", "INTRSCT_OP", "UNT_OP"}

ds_objects = {
    "STRING_CONSTANT", "CHARACTER_CONSTANT", "INT_CONST", "FLOAT_CONST", "IDENTIFIER"
}

# Check declaration grammar
def parse_declaration(number_line, tokens, lexemes, lines, result, Node):
    # Stores data type token[0] and number line[1] to popped_datatype
    popped_declaration = pop_first_element(number_line, tokens, lexemes)
    declaration = Node("Declaration", [Node(popped_declaration[0], [popped_declaration[2]])])

    # If data type is followed by an identifier
    if tokens and tokens[0] == "IDENTIFIER":
        # Stores identifier token[0] and number line[1] to popped_identifier
        popped_identifier = pop_first_element(number_line, tokens, lexemes)
        identifier = Node("Identifier", [popped_identifier[2]])

        if tokens and tokens[0] == "LPAREN":
            node, lines, result = parse_function(declaration, identifier, number_line, tokens, lexemes, lines, result, Node)
            return node, lines, result

        # If identifer is followed by comma, multiple declaration
        elif tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
            multichild_node, lines, result = parse_multidec(identifier, number_line, tokens, lexemes, lines, result, Node)
            node = Node("Declaration", [declaration, multichild_node])
            return node, lines, result
        
        elif tokens and tokens[0] == "LBRACKET":
            node, lines, result = parse_array(identifier, number_line, tokens, lexemes, lines, result, Node)
            return node, lines, result
        
        # If assignment
        elif tokens and tokens[0] in assignment_operators:
            node, lines, result = declaration_assignment(identifier, number_line, tokens, lexemes, lines, result, Node)
            return node, lines, result
        
        elif tokens and tokens[0] == "INSRT_OP" or tokens and tokens[0] == "PRTYEQ_OP":
            node, lines, result = parse_dscodeop(identifier, number_line, tokens, lexemes, lines, result, Node)
            return node, lines, result
        
        # If identifier is followed by a semicolon
        elif tokens and tokens[0] == "SEMICOLON":
            node = Node("Declaration", [identifier])
            popped_semicolon = pop_first_element(number_line, tokens, lexemes)
            return node, lines.append(popped_semicolon[1]), result
        
        else:
            if tokens:
                node = Node("Declaration", [identifier[0], Node("Error", [])])
                error_expected_after(lines, popped_identifier[1], result, "Assignment Operators, [, ;", "Identifier in declaration")
                return node, lines.append(popped_identifier[1]), result
            else:   
                node = Node("Declaration", [identifier[0], Node("Error", [])])
                error_expected_after(lines, popped_identifier[1], result, "Assignment Operators, [, ;", "Identifier in declaration")
                return node, lines.append(popped_identifier[1]), result

    # Error if data type is not followed by an identifier
    else:
        node = Node("Declaration", [Node("Error", [])])
        error_expected_after(lines, popped_declaration[1], result, "Identifier", "Declaration")
        return node, lines.append(popped_declaration[1]), result
        
def parse_function(datatype, identifier, number_line, tokens, lexemes, lines, result, Node):
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        if tokens:
            parameters, lines, result = parse_parameters(popped_lparen, number_line, tokens, lexemes, lines, result, Node)

            if tokens and tokens[0] == "SEMICOLON":
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                node = Node("Function", [datatype, identifier, parameters])
                return node, lines.append(popped_semicolon[1]), result
            elif tokens and tokens[0] == "LBRACE":
                function_body, lines, result = parse_statements(number_line, tokens, lexemes, lines, result, Node)
                node = Node("Function", [datatype, identifier, parameters, function_body])
                return node, lines, result
            elif tokens:
                #error in parameter, no semicollon/rbrace
                node = Node("Parameters", [Node("Error", [])])
                error_expected_after(lines, popped_lparen[1], result, "{ or ;", "parameters")
                return node, lines, result
            else:
                #error in Declaration, missing semicolon
                node = Node("Declaration", [("Error", [])])
                error_missing_semicolon(lines, popped_lparen[1], result, ";", "declaration")
                return node, lines, result
        else: 
            #error in function declarators when error in parameters
            node = Node("FunctionDeclaration", [Node("Error", [])])
            error_expected_after(lines, popped_lparen[1], result, "Parameters", "FunctionDeclaration")
            return node, lines.append(popped_lparen[1]), result
    
    

def parse_parameters(lparen, number_line, tokens, lexemes, lines, result, Node):
    parameters = []

    while tokens and tokens[0] != "RPAREN":
        if tokens and tokens[0] == "DATATYPE_KW":
            popped_datatype = pop_first_element(number_line, tokens, lexemes)
            if tokens and tokens[0] == "IDENTIFIER":
                popped_identifier = pop_first_element(number_line, tokens, lexemes)
                if tokens and tokens[0] == "COMMA":
                    pop_first_element(number_line, tokens, lexemes)
                    parameters.append(Node("Parameter", [popped_datatype, popped_identifier]))
                    continue
                else:
                    break
            else:
                node = Node("DataType", Node[("Error", [])])
                error_expected_after(lines, popped_datatype[1], result, "Identifier", "DataType")
                return node, lines.append(popped_datatype[1]), result      
        else:
            #error in data type
            pop_first_element(number_line, tokens, lexemes)
            node = Node("DataType", Node[("Error", [])])
            error_expected_after(lines, lparen[1], result, "DataType", "(")
            return node, lines.append(lparen[1]), result    

    if tokens and tokens[0] == "RPAREN":
        if parameters:
            popped_rparen = pop_first_element(number_line, tokens, lexemes)
            node = [Node("Parameters", [id]) for id in parameters]
            return node, lines.append(popped_rparen[1]), result
        else:
            node = Node("Parameterless", [])
            popped_rparen = pop_first_element(number_line, tokens, lexemes)
            return node, lines.append(popped_rparen[1]), result
    else:
        #error in parameters, no )
        node = Node("Parameters", [Node("Error", [])])
        error_expected_after(lines, lparen[1], result, ")", "parameters")
        return node, lines.append(popped_identifier[1]), result
        

def parse_multidec(popped_identifier, number_line, tokens, lexemes, lines, result, Node):
    nodes = [popped_identifier]

    if tokens and tokens[0] == "IDENTIFIER":
        while tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            nodes.append(popped_identifier)

            # Check if the identifier is followed by an assignment operator
            if tokens and tokens[0] in assignment_operators:
                popped_operator = pop_first_element(number_line, tokens, lexemes)
                expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
                nodes.append(Node("Assignment", [popped_identifier, popped_operator, expression]))

            # Check if there is another identifier after comma
            if tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
            else:
                break

        # If the last identifier is followed by a semicolon
        if tokens and tokens[0] == "SEMICOLON":
            end = pop_first_element(number_line, tokens, lexemes)
            # Include the current identifiers and their assignments in the Node
            node = [Node("DecNodes", [id]) for id in nodes]
            return node, lines.append(end[1]), result
        
        else:
            #error in declaration, no semicolon
            node = Node("Declaration", [Node("Error", [])])
            error_missing_semicolon(lines, popped_identifier[1], result, "Declaration")
            return node, lines.append(popped_identifier[1]), result
    else:
        #error in identifier, no comma
        node = Node("Identifier", [Node("Error", [])])
        error_expected_after(lines, popped_identifier[1], result, "Identifier", ",")
        return node, lines.append(popped_identifier[1]), result

def declaration_assignment(popped_identifier, number_line, tokens, lexemes, lines, result, Node):
    assignments = []

    while ((tokens and tokens[0] in assignment_operators) or (tokens and tokens[0] == "IDENTIFIER")):
        # Check if the identifier is followed by an assignment operator
        if tokens and tokens[0] in assignment_operators:
            popped_operator = pop_first_element(number_line, tokens, lexemes)
            expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
            assignments.append([popped_identifier, popped_operator[0], expression[0]])

            if tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
            else:
                continue
        elif tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            if tokens and tokens[0] in assignment_operators:
                continue
            elif tokens and tokens[0] == "COMMA":
                pop_first_element(number_line, tokens, lexemes)
                assignments.append(Node("DecNodes", [popped_identifier]))
        else:
            # Error: Expected assignment operator after identifier
            error_expected_after(lines, popped_identifier[1], result, "'='", "IdentifierInAssignment")
            break

    # If expression is followed by semicolon
    if tokens and tokens[0] == "SEMICOLON":
        node = [Node("Assignment", [id]) for id in assignments]
        end = pop_first_element(number_line, tokens, lexemes)
        return node, lines.append(end[1]), result

    # Error if assignment is missing semicolon
    else:
        node = Node("Assignment", [Node("Error", [])])
        error_missing_semicolon(lines, popped_operator[1], result, ";", "Assignment")
        return node, lines.append(popped_operator[1]), result

def parse_array(poppedidentifier, number_line, tokens, lexemes, lines, result, Node):
    identifier = poppedidentifier

    if tokens and tokens[0] == "LBRACKET":
        lbracket = pop_first_element(number_line, tokens, lexemes)
        if tokens:
            expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)
        else: 
            node = Node("Error", [Node("expression", [])])
            error_expected_after(lines, lbracket[1], result, "expression", "ArrayExpression")
            return node, lines.append(lbracket[1]), result
            
        if tokens and tokens[0] == "RBRACKET":
            rbracket = pop_first_element(number_line, tokens, lexemes)
            node = Node("Array", [identifier, lbracket, expression, rbracket])
            return node, lines.append(rbracket[1]), result
        
        #Error in array expression.
        else:
            node = Node("ArrayExpression", [Node("Error", [])])
            error_expected_after(lines, lbracket[1], result, "]", "ArrayExpression")
            return node, lines.append(lbracket[1]), result
    
def parse_dscodeop(popped_identifier, number_line, tokens, lexemes, lines, result, Node):
    nodes = []

    while tokens and tokens[0] == "INSRT_OP" or tokens and tokens[0] == "PRTYEQ_OP":
        pop_first_element(number_line, tokens, lexemes)

        if tokens and tokens[0] in ds_objects:
            dsobjects = pop_first_element(number_line, tokens, lexemes)
            nodes.append(Node("Insert", [popped_identifier, dsobjects[0]]))

            if tokens:
                if tokens and tokens[0] == "SEMICOLON":
                    end = pop_first_element(number_line, tokens, lexemes)
                    node = [Node("DSNodes", [id]) for id in nodes]
                    return node, lines.append(end[1]), result
                
                elif tokens and tokens[0] == "INSRT_OP" or tokens and tokens[0] == "PRTYEQ_OP":
                    continue

                else:
                    break
            
            #Error in declaration.
            else:
                node = Node("Declaration", [Node("Error", [])])
                error_missing_semicolon(lines, popped_identifier[1], result, "Declaration")
                return node, lines.append(popped_identifier[1]), result
        
        #Error in insert operation.
        else:
            node = Node("InsertOperation", [Node("Error", [])])
            error_expected_after(lines, popped_identifier[1], result, "ManyOthers", "InsertOperation")
            return node, lines.append(popped_identifier[1]), result

def parse_otherkeywords(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "print":
        return parse_print(number_line, tokens, lexemes, lines, result, Node)
    elif lexemes[0] == "const":
        return parse_const(number_line, tokens, lexemes, lines, result, Node)
    elif lexemes[0] == "input":
        return parse_input(number_line, tokens, lexemes, lines, result, Node)
    
# Const Keyword
def parse_const(number_line, tokens, lexemes, lines, result, Node):
    popped_const = pop_first_element(number_line, tokens, lexemes)
    
     # Check if const is followed by a datatype
    if tokens and tokens[0] == "DATATYPE_KW":
        popped_datatype = pop_first_element(number_line, tokens, lexemes)
        datatype = Node("DataType", [popped_datatype[2]])

        # Check if data type is followed by an identifier
        if tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            identifier = Node("Identifier", [popped_identifier[2]])
            
            # If identifier is followed by a semicolon
            if tokens and tokens[0] == "SEMICOLON":
                node = Node("Const", [datatype, identifier])
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                return node, lines.append(popped_semicolon[1]), result
            
            # Error if missing semicolon
            else:
                node = Node("Const", [datatype, identifier, Node("Error", [])])
                error_missing_semicolon(lines, popped_identifier[1], result, "const")
                return node, lines.append(popped_identifier[1]), result
            
        # Error if missing identifier
        else:
            node = Node("Const", [datatype, Node("Error", [])])
            error_expected_after(lines, popped_datatype[1], result, "Identifier", "Data Type")
            return node, lines.append(popped_datatype[1]), result

    # Error if const is not followed by a datatype 
    else:
        node = Node("Const", [Node("Error", [])])
        error_expected_after(lines, popped_const[1], result, "Data Type", "Const")
        return node, lines.append(popped_const[1]), result
    
#Input Keyword
def parse_input(number_line, tokens, lexemes, lines, result, Node):
    popped_input = pop_first_element(number_line, tokens, lexemes)

    # Check if inputt keyword is followed by left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        
        if tokens:
            argument = input_argument(number_line, tokens, lexemes, lines, result, Node)

            # Check if left parenthesis is followed by an input argument
            if not argument[0]:
                
                # Check if input argument is followed by right parenthesis
                if tokens and tokens[0] == "RPAREN":
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)

                    # Check if statement ends in semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Input", [argument[0]])
                        popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                        return node, lines.append(popped_semicolon[1]), result
                    
                    # Error for missing semicolon
                    else:
                        node = Node("Input", [argument[0], Node("Error", [])])
                        error_missing_semicolon(lines, popped_rparen[1], result, "')'")
                        return node, lines.append(popped_rparen[1]), result
                
                # Error for missing right parenthesis
                else:
                    node = Node("Input", [argument[0], Node("Error", [])])
                    error_expected_after(lines, popped_lparen[1], result, "')'", "input argument")
                    return node, lines.append(popped_lparen[1]), result
            
            # Error for missing input argument
            else:
                node = argument[0]
                error_expected_after(lines, argument[1], result, "identifier", "'('")
                return node, lines.append(argument[1]), result
        else:
            node = Node("Input", [Node("Error", [])])
            error_expected_after(lines, popped_lparen[1], result, "identifier", "'('")
            return node, lines.append(popped_lparen[1]), result    

    # Error for inavlid syntax   
    else:
        node = Node("Input", [Node("Error", [])])
        error_expected_after(lines, popped_input[1], result, "'('", "input keyword")
        return node, lines.append(popped_input[1]), result
    
def input_argument(number_line, tokens, lexemes, lines, result, Node):
    arguments = []
    
    while tokens and tokens[0] != "RPAREN":
        # Check if the token is an identifier
        if tokens and tokens[0] == "IDENTIFIER":
            argument_content = pop_first_element(number_line, tokens, lexemes)

        # Error if the token is not an identifier
        else:
            argument_content = pop_first_element(number_line, tokens, lexemes)
            
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "identifier", "input argument")
            return node, lines.append(argument_content[1]), result
    
        arguments.append(argument_content[0])
        # Check for comma for multiple arguments
        if tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
        # Check if the next token is a right parenthesis, indicating the end of arguments
        elif tokens and tokens[0] == "RPAREN":
            break
        # Error if there is an unexpected token after an argument
        else:
            
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "',' or ')'", argument_content[2])
            return node, lines.append(argument_content[1]), result
        
    if tokens:
        if tokens and tokens[0] == "RPAREN":
            node = [Node("Arguments", [id]) for id in arguments]
            return node, lines.append(argument_content[1]), result
    else:
        
        node = [Node("Arguments", [id]) for id in arguments]
        error_expected_after(lines, argument_content[1], result, "identifier", "'" + argument_content[2] + "'")
        return node, lines.append(argument_content[1]), result 


# Print Keyword
def parse_print(number_line, tokens, lexemes, lines, result, Node):
    popped_print = pop_first_element(number_line, tokens, lexemes)

    # Check if print keyword is followed by left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)

        if tokens:
            argument = print_argument(number_line, tokens, lexemes, lines, result, Node)

            # Check if left parenthesis is followed by a print argument
            if argument[0]:

                # Check if print argument is followed by righ parenthesis
                if tokens and tokens[0] == "RPAREN":
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)

                    # Check if statement ends in semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Print", [argument[0]])
                        popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                        return node, lines.append(popped_semicolon[1]), result
                    
                    # Error for missing semicolon
                    else:
                        node = Node("Print", [argument[0], Node("Error", [])])
                        error_missing_semicolon(lines, popped_rparen[1], result, "')'")
                        return node, lines.append(popped_rparen[1]), result
                
                # Error for missing right parenthesis
                else:
                    node = Node("Print", [argument[0], Node("Error", [])])
                    error_expected_after(lines, popped_lparen[1], result, "')'", "print argument")
                    return node, lines.append(popped_lparen[1]), result
            
            # Error for missing print argument
            else:
                node = argument[0]
                return node, lines.append(argument[1]), result
        else:
            node = Node("Print", [Node("Error", [])])
            error_expected_after(lines, popped_lparen[1], result, "string literal or identifier", "'('")
            return node, lines, result

    # Error for inavlid syntax   
    else:
        node = Node("Print", [Node("Error", [])])
        error_expected_after(lines, popped_print[1], result, "'('", "print keyword")
        return node, lines, result

def print_argument(number_line, tokens, lexemes, lines, result, Node):
    arguments = []
    
    while tokens and tokens[0] != "RPAREN":
        # Check if the token is a string constant
        if tokens and tokens[0] == "STRING_CONSTANT":
            argument_content = pop_first_element(number_line, tokens, lexemes)

        # Check if the token is an identifier    
        elif tokens and tokens[0] == "IDENTIFIER":
            argument_content = pop_first_element(number_line, tokens, lexemes)

        # Error if the token is neither a string constant nor an identifier
        else:
            argument_content = pop_first_element(number_line, tokens, lexemes)
            arguments.append(Node("Error", [argument_content[0]]))
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "string literal or identifier", "print argument")
            return node, lines.append(argument_content[1]), result
    
        arguments.append(argument_content[0])
        # Check for comma between multiple arguments
        if tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
        # Check if the next token is a right parenthesis, indicating the end of arguments
        elif tokens and tokens[0] == "RPAREN":
            break
        # Error if there is an unexpected token after an argument
        else:
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "',' or ')'", argument_content[2])
            return node, lines.append(argument_content[1]), result
        
    if tokens:
        # Check if the right parenthesis is present, indicating the end of arguments
        if tokens and tokens[0] == "RPAREN":
            node = [Node("Arguments", [id]) for id in arguments]
            return node, lines.append(argument_content[1]), result
    else:
        # Error if there are no tokens left and the function unexpectedly ends
        node = [Node("Arguments", [id]) for id in arguments]
        error_expected_after(lines, argument_content[1], result, "string literal or identifier", "'" + argument_content[2] + "'")
        return node, lines.append(argument_content[1]), result 