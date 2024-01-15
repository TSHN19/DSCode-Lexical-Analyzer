# KEYWORDS
TT_ControlFlowKeywords = {
    "break", 
    "continue",
    "do",
    "else", 
    "for",
    "goto",
    "if", 
    "return",
    "switch", 
    "while"
}   

TT_DataTypeKeywords = {
    "char", 
    "double", 
    "enum", 
    "float", 
    "int", 
    "long", 
    "short", 
    "signed",
    "struct", 
    "union",
    "unsigned", 
    "void"
}

TT_StorageClassKeywords = {
    "auto", 
    "extern",
    "register", 
    "static", 
    "typedef"
}

TT_OtherKeywords = {
    "case", 
    "const", 
    "default", 
    "sizeof", 
    "volatile"
}

# OPERATORS
TT_Operators = [
    ('+', "Plus"),
    ('-', "Minus"),
    ('*', "Multiply/Asterisk"),
    ('/', "Divided By"),
    ('%', "Modulo/Remainder"),
    ('>', "Greater Than"),
    ('<', "Less Than"),
    ('!', "Logical NOT"),
    ('=', "Assignment"),
    ('&', "Bitwise AND"),
    ('|', "Bitwise OR"),
    ('^', "Bitwise XOR"),
    ('~', "Bitwise NOT/Tilde"),
    ('+=', "Addition Assignment"),
    ('++', "Increment"),
    ('-=', "Subtraction Assignment"),
    ('--', "Decrement"),
    ('*=', "Multiplication Assignment"),
    ('/=', "Division Assignment"),
    ('%=', "Modulo Assignment"),
    ('>=', "Greater Than or Equal To"),
    ('>>', "Right Shift"),
    ('>>=', "Right Shift Assignment"),
    ('<=', "Less Than or Equal To"),
    ('<<', "Left Shift"),
    ('<<=', "Left Shift Assignment"),
    ('!=', "Not equal To"),
    ('==', "Equal To",),
    ('&&', "Logical AND"),
    ('&=', "Bitwise AND Assignment"),
    ('||', "Logical OR"),
    ('|=', "Bitwise OR Assignment"),
    ('^=', "Bitwise XOR Assignment")
]

TT_SpecialSymbols = [
    ('[', "Left Bracket"),
    (']', "Right Bracket"),
    ('(', "Left Parenthesis"),
    (')', "Right Parenthesis"),
    ('{', "Left Brace"),
    ('}', "Right Brace"),
    (',', "Comma"),
    (':', "Colon"),
    (';', "Semicolon"),
    ('#', "Pre-Processor"),
    ('.', "Period"),
    ('[]', "Brackets"),
    ('()', "Parenthesis"),
    ('{}', "Braces")
]
