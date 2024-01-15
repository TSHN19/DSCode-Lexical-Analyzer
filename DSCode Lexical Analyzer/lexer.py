from tokentypes import TT_SpecialSymbols, TT_Operators, TT_ControlFlowKeywords, TT_DataTypeKeywords, TT_StorageClassKeywords, TT_OtherKeywords
    
def lexical_analyzer(code):
    lexemes = []
    lexemes_display = []
    tokens = []
    current_token = ''
    invalid_token = ''
    string_delimiter_count = 0
    in_string = False
    double_operator = False
    triple_operator = False

    operatorSymbols = [symbol for symbol, _ in TT_Operators]
    specialSymbols = [symbol for symbol, _ in TT_SpecialSymbols]
    controlflow = list(TT_ControlFlowKeywords)
    datatype = list(TT_DataTypeKeywords)
    storageclass = list(TT_StorageClassKeywords)
    otherkeywords = list(TT_OtherKeywords)
    
    # Iterate through each character in the code
    for i in range(len(code)):
        char = code[i]

        # Check if the character is blank
        if ((char == ' ') or (char == '\n') or (char == '\t')) and in_string is False:
            continue

        # Check for invalid tokens
         # This part of the lexical for digit when identifying an identifier with number as the start
         # This is to skip the remaining char for an identifier with number as the start
        elif char in invalid_token:
            invalid_token = invalid_token[1:]
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
                lexemes.append("ERROR: Invalid Token")
                lexemes_display.append(string_char + '...')

            elif string_delimiter_count == 2:
                lexemes[-1] = current_token
                string_display = current_token[1 : -1]
                lexemes_display[-1] = string_char + string_display[:2] + '...' + char
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
                    lexemes_display.append(current_token)
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
                lexemes_display.append(current_token + char)
                double_operator = not double_operator

            else:
                # Get the index of char in the single operators list
                index = operatorSymbols.index(char)
                lexemes.append(char)
                lexemes_display.append(char)

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
                lexemes_display.append(current_token + char)
                double_operator = not double_operator

            else:
                # Get the index of char in the single operators list
                index = specialSymbols.index(char)
                lexemes.append(char)
                lexemes_display.append(char)

            # Use the index to access the corresponding token description
            token_description = TT_SpecialSymbols[index][1]
            tokens.append(token_description)
            current_token = ''

        #KEYWORDS AND IDENTIFIER
            
        # Checks if the char is alphabet, _, or a digit 
        # accepts the digit only if the current token is not empty meaning there is a word before the number
        # and when the current token is not all digits(need kasi na pag digits sa number sha)
        elif char.isalpha() or char == '_' or (char.isdigit() and current_token != '' and not current_token.isdigit):
            # The character is alphabetical, _, add it to the current token
            current_token += char
            if (i + 1 < len(code)) and (not code[i + 1].isalnum() and code[i + 1] != '_'):
                # Check if the current token is a data type keyword
                if current_token in datatype:
                    lexemes.append(current_token)
                    tokens.append("Data Type")
                    current_token = ''

                elif current_token in controlflow:
                    lexemes.append(current_token)
                    tokens.append("Control Flow")
                    current_token = ''
                    
                elif current_token in storageclass:
                    lexemes.append(current_token)
                    tokens.append("Storage Class")
                    current_token = ''

                elif current_token in otherkeywords:
                    lexemes.append(current_token)
                    tokens.append("Other Keywords")
                    current_token = ''

                else:
                    # The current token is not a data type keyword, treat as an identifier
                    lexemes.append(current_token)
                    tokens.append("Identifier")
                    current_token = ''
            else: continue
        
        #If char is a number
        elif char.isdigit() or char == '.':
            current_token += char
            # This is to check whether the digit is followed by a alphabet or _ (since bawal nga sha sa rule ng identifier)
            # if yes then papasok sha sa loop
            if (i + 1 < len(code)) and (code[i + 1].isalpha() or code[i + 1]=='_'):
                j = i
                # this loop is to iterate until the final char in the identifier is read
                # eg identifier: 2try
                # babasahin nya hanggang y
                while (code[j + 1].isalnum() or code[j + 1]=='_'):
                    current_token += code[j + 1]
                    j+=1
                lexemes.append(current_token)
                tokens.append("ERROR: Invalid Token")

                # eto yung invalid token sa taas, pinasa sha para lagpasan na lang yung part pa nung identifier
                invalid_token = current_token
                current_token = current_token[1:]
                current_token = ''

            #pa add na lang ako here paano yung sa float
            elif (i + 1 < len(code)) and (not code[i + 1].isdigit() and code[i + 1] != '.'):
                lexemes.append(current_token)
                tokens.append("Digit")
                current_token = ''

            else:
                continue

        else:
            lexemes.append(char)
            lexemes_display.append(char)
            tokens.append("ERROR: Invalid Token")
            current_token = ''
    
    return lexemes_display, tokens
