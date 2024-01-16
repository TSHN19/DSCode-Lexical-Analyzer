alphabet = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

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
    "void",
    "stack",
    "llist",
    "queue"
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
    "pqueue",
    "peek",
    "input",
    "print"
}

# OPERATORS
TT_Operators = [
    ('+', "Plus Operator"),
    ('-', "Minus Operator"),
    ('*', "Multiply/Asterisk Operator"),
    ('/', "Divided By Operator"),
    ('%', "Modulo/Remainder Operator"),
    ('>', "Greater Than Operator"),
    ('<', "Less Than Operator"),
    ('!', "Logical NOT Operator"),
    ('=', "Assignment Operator"),
    ('&', "Bitwise AND Operator"),
    ('|', "Bitwise OR Operator"),
    ('^', "Bitwise XOR Operator"),
    ('~', "Bitwise NOT/Tilde Operator"),
    ('+=', "Addition Assignment Operator"),
    ('++', "Increment Operator"),
    ('-=', "Subtraction Assignment Operator"),
    ('--', "Decrement Operator"),
    ('*=', "Multiplication Assignment Operator"),
    ('/=', "Division Assignment Operator"),
    ('%=', "Modulo Assignment Operator"),
    ('>=', "Greater Than or Equal To Operator"),
    ('>>', "Right Shift Operator"),
    ('>>=', "Right Shift Assignment Operator"),
    ('<=', "Less Than or Equal To Operator"),
    ('<<', "Left Shift Operator"),
    ('<<=', "Left Shift Assignment Operator"),
    ('!=', "Not equal To Operator"),
    ('==', "Equal To Operator"),
    ('&&', "Logical AND Operator"),
    ('&=', "Bitwise AND Assignment Operator"),
    ('||', "Logical OR Operator"),
    ('|=', "Bitwise OR Assignment Operator"),
    ('^=', "Bitwise XOR Assignment Operator"),
    ('<+', "Enqueue Operator"),
    ('>-', "Dequeue Operator"),
    ('>->', "Recursive Dequeue Operator"),
    ('<+<', "Priority Enqueue Operator"),
    ('>|<', "Intersect Operator"),
    ('#&#', "Unite Operator"),
    ('??', "Search Operator"),
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
    ('{}', "Braces"),
]

