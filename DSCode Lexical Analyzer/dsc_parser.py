from tokentypes import TT_Operators, TT_Delimiters
from grammar import G_ForLoop

for_loop = False

g_forloop = list(G_ForLoop)

def syntax_analyzer(number_line, tokens, lexemes):

    invalid_token = "ERROR"
    parser_result = []
    parser_lines = []

    symbols = [symbol for symbol, _ in TT_Operators] 
    delimiters = [symbol for symbol, _ in TT_Delimiters]

    # Iterate through each tokens
    for i in range(len(tokens)):
        current_token = tokens[i]
        current_line = number_line[i]
        current_lexeme = lexemes[i]

        # Print error if current token is invalid
        if invalid_token in current_token:
            parser_result.append("Invalid Token")
            parser_lines.append(current_line)

        elif current_lexeme in symbols:
            symbol_handling(current_token)
        
        # "break", "continue", "do", "else", "for","goto","if", "return","switch", "while"
        elif current_token == "CTRLFLOW_KW":
            if current_lexeme == "for":
                for_loop = not for_loop
                j = 1


    return parser_lines, parser_result

def symbol_handling(current_token):
    if current_token == "LPAREN":
        if for_loop is True:
            return
    
    elif current_token == "SEMICOLON":
        if for_loop is True:
            return

