from tokentypes import TT_SpecialSymbols, TT_Operators
    
def lexical_analyzer(code):
    lexemes = []
    tokens = []
    current_token = ''
    string_delimiter_count = 0
    in_string = False
    double_operator = False
    triple_operator = False

    operatorSymbols = [symbol for symbol, _ in TT_Operators]
    specialSymbols = [symbol for symbol, _ in TT_SpecialSymbols]
    
    # Iterate through each character in the code
    for i in range(len(code)):
        char = code[i]

        # Check if the character is blank
        if (char == ' ') or (char == '\n') or (char == '\t'):
            continue
        
        # Check if the character is a string delimiter
        elif (char == '"') or (char == "'"):
            # Toggle string mode 
            in_string = not in_string
            string_delimiter_count += 1
            current_token += char

            if string_delimiter_count == 1:
                tokens.append("ERROR: Incomplete String Closing Delimiter(" + char + ")")
                string_char = char
                lexemes.append(string_char + '...')

            elif string_delimiter_count == 2:
                lexeme_display = current_token[1 : -1]
                lexemes[-1] = string_char + lexeme_display[:2] + '...' + char
                string_delimiter_count = 0
                current_token = ''

                if string_char == char:
                    tokens[-1] = "String"
                else:
                    tokens[-1] = "ERROR: Different String Delimiters Employed"
        
        elif in_string:
            # Inside a string literal
            current_token += char
        

        # ----Fix three operators, separate 
        elif char in operatorSymbols:
            
            # Check if character is part of a three symbol operator
            if (len(code) > i + 2) and ((char + code[i + 1] + code[i + 2]) in operatorSymbols):
                triple_operator = not triple_operator
                # Build token
                current_token += char
                continue

            elif triple_operator:
                # Build token
                current_token += char
                
                if len(current_token) == 3:
                    print(current_token)
                    # index = operatorSymbols.index(current_token)
                    lexemes.append(current_token)
                    triple_operator = not triple_operator

            elif (char + code[i + 1]) in operatorSymbols and (double_operator is False):
                # Build token
                current_token += char
                double_operator = not double_operator
                continue
            
            elif double_operator:
                # Get the index of char in the double operators list
                index = operatorSymbols.index(current_token + char)
                lexemes.append(current_token + char)
                double_operator = not double_operator

            else:
                # Get the index of char in the single operators list
                index = operatorSymbols.index(char)
                lexemes.append(char)

            # Use the index to access the corresponding token description
            token_description = TT_Operators[index][1]
            tokens.append(token_description + " Operator")
            current_token = ''
        
        elif char in specialSymbols:
            if (char + code[i + 1]) in specialSymbols and (double_operator is False):
                # Build token
                current_token += char
                double_operator = not double_operator
                continue
            
            elif double_operator:
                # Get the index of char in the special symbols list
                index = specialSymbols.index(current_token + char)
                lexemes.append(current_token + char)
                double_operator = not double_operator

            else:
                # Get the index of char in the single operators list
                index = specialSymbols.index(char)
                lexemes.append(char)

            # Use the index to access the corresponding token description
            token_description = TT_SpecialSymbols[index][1]
            tokens.append(token_description)
            current_token = ''

        else:
            lexemes.append(char)
            tokens.append("ERROR: Invalid Token")
            current_token = ''
    
    return lexemes, tokens
