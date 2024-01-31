G_Operand = {"IDENTIFIER", "FLOAT_CONST", "INT_CONST"}

G_BooleanOperators = {
    # Relational Operators
    "EQLTO_OP", "NOTEQLTO_OP", "GRTRTHN_OP", "LSSTHN_OP", "GRTREQL_OP", "LSSEQL_OP",

    # Logical Operators
    "LOGNOT_OP", "LOGAND_OP", "LOGOR_OP",

    # Bitwise Operators
    "BTWAND_OP", "BTWOR_OP", "BTWXOR_OP", "BTWNOT_OP"}

G_Boolean = {"operand", "boolean_operators"}
G_ForLoop = {"for", "LPAREN", "EXPR", "SEMICOLON", "BOOL", "SEMICOLON", "EXPR", "RPAREN", "LBRACE", "STATEMENTS", "RBRACE"}