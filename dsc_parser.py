from tokentypes import TT_Operators, TT_Delimiters
from grammar import G_Operand

parser_result = []
parser_lines = []

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def syntax_analyzer(number_line, tokens, lexemes):
    parser_result = []
    parser_lines = []
    statements = []
    number_line_copy = number_line
    tokens_copy = tokens
    lexemes_copy = lexemes

    # Iterate through each tokens
    while tokens_copy:
        if "ERROR" in tokens_copy[0]:
            parser_lines.append(number_line_copy.pop(0))
            parser_result.append("Invalid Token")
            tokens_copy.pop(0)
            lexemes_copy.pop(0)

        elif tokens_copy[0] == "DATATYPE_KW":
            statements.append(parse_declaration(number_line_copy, tokens_copy, lexemes_copy))    

        elif tokens_copy[0] == "CTRLFLOW_KW":
            statements.append(parse_controlflow(number_line_copy, tokens_copy, lexemes_copy))

        elif tokens_copy[0] == "KEYWORD":
            statements.append(parse_otherkeywords(number_line_copy, tokens_copy, lexemes_copy))
        
        elif tokens_copy[0] == "IDENTIFIER":
            statements.append(parse_assignment(number_line_copy, tokens_copy, lexemes_copy))

        else:
            parser_lines.append(number_line_copy.pop(0))
            parser_result.append("SYNTAX ERROR")
            tokens_copy.pop(0)
            lexemes_copy.pop(0)

    # return Node("Program", statements)
    return parser_lines, parser_result

def pop_first_element(number_line, tokens, lexemes):
    tokens.pop(0)
    lexemes.pop(0)
    number_line_value = number_line.pop(0)
    return number_line_value

def parse_declaration(number_line, tokens, lexemes):
    return

def parse_controlflow(number_line, tokens, lexemes):
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
            initialization = parse_statement(number_line, tokens, lexemes)

            if tokens[0] == "SEMICOLON":
                semicolon_line_value = pop_first_element(number_line, tokens, lexemes)
                condition = parse_expression(number_line, tokens, lexemes)

                if tokens[0] == "SEMICOLON":
                    semicolon2_line_value = pop_first_element(number_line, tokens, lexemes)
                    increment = parse_expression(number_line, tokens, lexemes)

                    if tokens[0] == "RPAREN":
                        pop_first_element(number_line, tokens, lexemes)
                        body = parse_statement(number_line, tokens, lexemes)
                        return Node("ForLoop", [initialization, condition, increment, body])
                    else:
                        parser_lines.append(semicolon2_line_value)
                        parser_result.append("Expected ')' after '(' in expression")

                else:
                    parser_lines.append(semicolon_line_value)
                    parser_result.append("Expected semicolon ';' after initialization")
            else:
                parser_lines.append(lparen_line_value)
                parser_result.append("Expected semicolon ';' after initialization")
            
        else:
            parser_lines.append(for_line_value)
            parser_result.append("Invalid for loop syntax")
    
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
            condition = parse_expression(tokens)
            
            if tokens[0] == "RPAREN":
                pop_first_element(number_line, tokens, lexemes)
                body = parse_statement(tokens)
                return Node("WhileLoop", [condition, body])

            else:
                parser_lines.append(lparen_line_value)
                parser_result.append("Expected ')' after '(' in expression")
                
        else:
            parser_lines.append(number_line_value)
            parser_result.append("Invalid for while loop syntax")


def parse_otherkeywords(number_line, tokens, lexemes):
    return

def parse_statement(number_line, tokens, lexemes):
    return

# Assignment, Addition, Subtraction, Multiplication, Division, Modulo, Bitwise (AND, OR, XOR), Right and Left Shift Assignment
def parse_assignment(number_line, tokens, lexemes):
    identifier = tokens.pop(0)
    lexemes.pop(0)
    number_line_value = number_line.pop(0)

    if tokens and tokens[0] in ("ASGN_OP", "ADDASGN_OP", "SUBASGN_OP", "MULTASGN_OP", "DIVASGN_OP", "MODASGN_OP", 
        "BTWANDASGN_OP","BTWORASGN_OP", "BTWXORASGN_OP", "RSHIFTASGN_OP", "LSHIFTASGN_OP", "INTRSCT_OP", "UNT_OP"):
        pop_first_element(number_line, tokens, lexemes)
        expression = parse_expression(number_line, tokens, lexemes)
        return Node("Assignment", [Node(identifier), expression])
    else:
        parser_lines.append(number_line_value)
        parser_result.append("Expected '=' after identifier in assignment")

def parse_identifier(number_line, tokens, lexemes):
    if tokens and tokens[0] == "IDENTIFIER":
        lexemes.pop(0)
        number_line.pop(0)
        return tokens.pop(0)
    else:
        parser_lines.append(number_line[0])
        parser_result.append("Expected identifier")


"""
E X P R E S S I O N S   H A N D L I N G
Check expressions and operators used following their order of precedence
    1. PARENTHESIS
    2. UNARY OPERATORS: ++, --, !, ~
    3. MULTIPLICATIVE OPERATORS: *, /, %
    4. ADDITIVE OPERATORS: +, -
    5. SHIFT OPERATORS: <<, >>
    6. RELATIONAL OPERATORS: <, >, <=, >=
    7. EQUALITY OPERATORS: !=, ==
    8. BITWISE AND OPERATOR: &
    9. BITWISE XOR OPERATOR: ^
    10.BITWISE OR OPERATOR: |
    11.LOGICAL AND OPERATOR: &&
    12.LOGICAL OR OPERATOR: ||

    Kulang: DSCODE Operators
"""

def parse_expression(number_line, tokens, lexemes):
    node = parse_logical_or(number_line, tokens, lexemes)
    return node

# Logical OR Operator
def parse_logical_or(number_line, tokens, lexemes):
    node = parse_logical_and(number_line, tokens, lexemes)

    while tokens and tokens[0] == "LOGOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_logical_and(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Logical AND Operator
def parse_logical_and(number_line, tokens, lexemes):
    node = parse_bitwise_or(number_line, tokens, lexemes)

    while tokens and tokens[0] == "LOGAND_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_or(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise OR Operator
def parse_bitwise_or(number_line, tokens, lexemes):
    node = parse_bitwise_xor(number_line, tokens, lexemes)

    while tokens and tokens[0] == "BTWOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_xor(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise XOR Operator
def parse_bitwise_xor(number_line, tokens, lexemes):
    node = parse_bitwise_and(number_line, tokens, lexemes)

    while tokens and tokens[0] == "BTWXOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_and(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise AND Operator
def parse_bitwise_and(number_line, tokens, lexemes):
    node = parse_equality(number_line, tokens, lexemes)

    while tokens and tokens[0] == "BTWAND_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_equality(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Not Equal To and Equal To Operators
def parse_equality(number_line, tokens, lexemes):
    node = parse_relational(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("NOTEQLTO_OP", "EQLTO_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_relational(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Greater Than, Less Than, Greater Than or Equal To, and Less Than or Equal To Operators
def parse_relational(number_line, tokens, lexemes):
    node = parse_shift(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("GRTRTHN_OP", "LSSTHN_OP", "GRTREQL_OP", "LSSEQL_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_shift(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Right Shift and Left Shift Operators
def parse_shift(number_line, tokens, lexemes):
    node = parse_additive(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("RSHIFT_OP", "LSHIFT_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_additive(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Plus and Minus Operators
def parse_additive(number_line, tokens, lexemes):
    node = parse_multiplicative(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("PLUS_OP", "MINUS_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_multiplicative(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Multiply, Divide, and Modulo Operators
def parse_multiplicative(number_line, tokens, lexemes):
    node = parse_unary(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("MULTIPLY_OP", "DIVIDE_OP", "MODULO_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_unary(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Increment, Decrement, Logical Not, and Bitwise Not Operators
def parse_unary(number_line, tokens, lexemes):
    node = parse_factor(number_line, tokens, lexemes)

    while tokens and tokens[0] in ("INCR_OP", "DECR_OP", "LOGNOT_OP", "BTWNOT_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_factor(number_line, tokens, lexemes)
        node = Node(operator, [node, right_node])
    
    return node

# Handle integer and float constants, identifiers, and parenthesis
def parse_factor(number_line, tokens, lexemes):
    if tokens[0] in ("INT_CONST", "FLOAT_CONST", "IDENTIFIER"):
        lexemes.pop(0)
        number_line.pop(0)
        return Node(tokens.pop(0))
    
    elif tokens[0] == "LPAREN":
        tokens.pop(0)
        lexemes.pop(0)
        number_line_value = number_line.pop(0)
        expression = parse_expression(number_line, tokens, lexemes)

        if tokens and tokens[0] == "RPAREN":
            tokens.pop(0)
            lexemes.pop(0)
            number_line.pop(0)
            return expression
        else:
            parser_lines.append(number_line_value)
            parser_result.append("Expected ')' after '(' in expression")
    
    else:
        parser_lines.append(number_line[0])
        parser_result.append(f"ERROR Unexpected token: {tokens[0]}")