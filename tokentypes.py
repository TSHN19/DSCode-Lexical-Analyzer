alphabet = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

noise_words = [
    "eger",
    "acter",
    "inked",
    "riority"
]

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
    "queue",
    "character",
    "integer",
    "linkedlist"
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
    "volatile",
    "peek",
    "input",
    "print"
}

# OPERATORS
TT_Operators = [
    ('+', "PLUS_OP"),
    ('-', "MINUS_OP"),
    ('*', "MULTIPLY_OP"),
    ('/', "DIVIDE_OP"),
    ('%', "MODULO_OP"),
    ('>', "GRTRTHN_OP"),
    ('<', "LSSTHN_OP"),
    ('!', "LOGNOT_OP"),
    ('=', "ASGN_OP"),
    ('&', "BTWAND_OP"),
    ('|', "BTWOR_OP"),
    ('^', "BTWXOR_OP"),
    ('?', "CONDTRNY_OP"),
    ('~', "BTWNOT_OP"),
    ('+=', "ADDASGN_OP"),
    ('++', "INCR_OP"),
    ('-=', "SUBASGN_OP"),
    ('--', "DECR_OP"),
    ('*=', "MULTASGN_OP"),
    ('/=', "DIVASGN_OP"),
    ('%=', "MODASGN_OP"),
    ('>=', "GRTREQL_OP"),
    ('>>', "RSHIFT_OP"),
    ('>>=', "RSHIFTASGN_OP"),
    ('<=', "LSSEQL_OP"),
    ('<<', "LSHIFT_OP"),
    ('<<=', "LSHIFTASGN_OP"),
    ('!=', "NOTEQLTO_OP"),
    ('==', "EQLTO_OP"),
    ('&&', "LOGAND_OP"),
    ('&=', "BTWANDASGN_OP"),
    ('||', "LOGOR_OP"),
    ('|=', "BTWORASGN_OP"),
    ('^=', "BTWXORASGN_OP"),
    ('<+', "INSRT_OP"),
    ('>-', "RMV_OP"),
    ('>->', "RCSVDQ_OP"),
    ('<+<', "PRTYEQ_OP"),
    ('>|<', "INTRSCT_OP"),
    ('#&#', "UNT_OP"),
    ('??', "SRCH_OP"),
    (',', "COMMA"),
    (':', "COLON"),
    (';', "SEMICOLON"),
    ('#', "PPROCESSOR"),
    ('.', "PERIOD"),
    ('[]', "BRACKETS"),
    ('()', "PARENTHESIS"),
    ('{}', "BRACES")
]

TT_Delimiters = [
    ('[', "LBRACKET"),
    (']', "RBRACKET"),
    ('(', "LPAREN"),
    (')', "RPAREN"),
    ('{', "LBRACE"),
    ('}', "RBRACE")
]

