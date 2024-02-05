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

def parse_expression(number_line, tokens, lexemes, lines, result, Node):
    node = parse_logical_or(number_line, tokens, lexemes, lines, result, Node)
    return node

# Logical OR Operator
def parse_logical_or(number_line, tokens, lexemes, lines, result, Node):
    node = parse_logical_and(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] == "LOGOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_logical_and(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Logical AND Operator
def parse_logical_and(number_line, tokens, lexemes, lines, result, Node):
    node = parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] == "LOGAND_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise OR Operator
def parse_bitwise_or(number_line, tokens, lexemes, lines, result, Node):
    node = parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] == "BTWOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise XOR Operator
def parse_bitwise_xor(number_line, tokens, lexemes, lines, result, Node):
    node = parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] == "BTWXOR_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Bitwise AND Operator
def parse_bitwise_and(number_line, tokens, lexemes, lines, result, Node):
    node = parse_equality(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] == "BTWAND_OP":
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_equality(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Not Equal To and Equal To Operators
def parse_equality(number_line, tokens, lexemes, lines, result, Node):
    node = parse_relational(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("NOTEQLTO_OP", "EQLTO_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_relational(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Greater Than, Less Than, Greater Than or Equal To, and Less Than or Equal To Operators
def parse_relational(number_line, tokens, lexemes, lines, result, Node):
    node = parse_shift(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("GRTRTHN_OP", "LSSTHN_OP", "GRTREQL_OP", "LSSEQL_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_shift(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Right Shift and Left Shift Operators
def parse_shift(number_line, tokens, lexemes, lines, result, Node):
    node = parse_additive(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("RSHIFT_OP", "LSHIFT_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_additive(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Plus and Minus Operators
def parse_additive(number_line, tokens, lexemes, lines, result, Node):
    node = parse_multiplicative(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("PLUS_OP", "MINUS_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_multiplicative(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Multiply, Divide, and Modulo Operators
def parse_multiplicative(number_line, tokens, lexemes, lines, result, Node):
    node = parse_unary(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("MULTIPLY_OP", "DIVIDE_OP", "MODULO_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_unary(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Increment, Decrement, Logical Not, and Bitwise Not Operators
def parse_unary(number_line, tokens, lexemes, lines, result, Node):
    node = parse_factor(number_line, tokens, lexemes, lines, result, Node)

    while tokens and tokens[0] in ("INCR_OP", "DECR_OP", "LOGNOT_OP", "BTWNOT_OP"):
        operator = tokens.pop(0)
        lexemes.pop(0)
        number_line.pop(0)
        right_node = parse_factor(number_line, tokens, lexemes, lines, result, Node)
        node = Node(operator, [node, right_node])
    
    return node

# Handle integer and float constants, identifiers, and parenthesis
def parse_factor(number_line, tokens, lexemes, lines, result, Node):
    if tokens[0] in ("INT_CONST", "FLOAT_CONST", "IDENTIFIER"):
        lexemes.pop(0)
        number_line.pop(0)
        return Node(tokens.pop(0))
    
    elif tokens[0] == "LPAREN":
        tokens.pop(0)
        lexemes.pop(0)
        number_line_value = number_line.pop(0)
        expression = parse_expression(number_line, tokens, lexemes, lines, result, Node)

        if tokens and tokens[0] == "RPAREN":
            tokens.pop(0)
            lexemes.pop(0)
            number_line.pop(0)
            return expression
        else:
            lines.append(number_line_value)
            result.append("Expected ')' after '(' in expression")
    
    else:
        lines.append(number_line[0])
        result.append(f"ERROR Unexpected token: {tokens[0]}")

