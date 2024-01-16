from tokentypes import TT_Operators, TT_ControlFlowKeywords, TT_DataTypeKeywords, TT_StorageClassKeywords, TT_OtherKeywords
from tokentypes import alphabet, digits
    
def lexical_analyzer(code):
    lexemes = []
    lexemes_display = []
    tokens_display = []
    current_token = ''
    invalid_token = ''
    string_delimiter_count = 0
    in_singlecomment = False
    in_multiplecomment = False
    in_string = False
    double_operator = False
    triple_operator = False

    symbols = [symbol for symbol, _ in TT_Operators]    
    controlflow = list(TT_ControlFlowKeywords)
    datatype = list(TT_DataTypeKeywords)
    storageclass = list(TT_StorageClassKeywords)
    otherkeywords = list(TT_OtherKeywords)

    
    # Iterate through each character in the code
    for i in range(len(code)):
        char = code[i]

        # Check if the character is blank
        if char == "/" and code[i + 1] == "/":
            current_token += char
            in_singlecomment = not in_singlecomment

        elif in_singlecomment and char == "\n":
            in_singlecomment = not in_singlecomment
            lexemes.append(current_token)
            lexemes_display.append(current_token)
            tokens_display.append("Single-Line Comment")
            current_token = ''

        elif char == "/" and code[i + 1] == "*":
            current_token += char
            in_multiplecomment = not in_multiplecomment

        elif in_multiplecomment and code[i - 1] == "*" and char == "/":
            current_token += char
            in_multiplecomment = not in_multiplecomment
            lexemes.append(current_token)
            lexemes_display.append(current_token)
            tokens_display.append("Multiple-Line Comment")
            current_token = ''
        
        elif in_singlecomment or in_multiplecomment:
            current_token += char

        elif ((char == ' ') or (char == '\n') or (char == '\t')) and not(in_string or in_singlecomment or in_multiplecomment):
            continue

        # Check if the character is a string delimiter
        elif (char == '"') or (char == "'"):
            # Toggle string mode 
            in_string = not in_string
            string_delimiter_count += 1
            current_token += char

            # Set as invalid, unless encounters a closing delimiter
            if string_delimiter_count == 1:
                tokens_display.append("ERROR: Incomplete String Closing Delimiter(" + char + ")")
                string_char = char
                lexemes.append("ERROR: Invalid Token")
                lexemes_display.append(string_char)

            # If encounters a closing delimiter, close the string input
            elif string_delimiter_count == 2:
                lexemes[-1] = current_token
                string_delimiter_count = 0

                # Check if string is a string literal
                if (string_char == char) and (string_char == '"'):
                    string_display = current_token[1 : -1]
                    lexemes_display[-1] = string_char + string_display[:9] + '...' + char
                    tokens_display[-1] = "String Constant"

                # Check if string uses single quotes delimiter
                elif (string_char == char) and (string_char == "'"):
                    # If the input is a single character
                    if len(current_token) == 3:
                        lexemes_display[-1] = current_token
                        tokens_display[-1] = "Character Constant"
                    
                    # Else, notify wrong delimiter used
                    else:
                        tokens_display[-1] = "ERROR: Character Literal Delimiter Used for String Literal"

                # Notify different string delimiters employed
                else:
                    tokens_display[-1] = "ERROR: Different String Delimiters Employed"
                
                current_token = ''
        
        # While in_string is true, all following inputs will count as String Literal
        elif in_string:
            # Inside a string literal
            current_token += char

            if len(current_token) < 14:
                lexemes_display[-1] = current_token[:10] + "...?"

        
        # Check if input is a operator or special symbol
        elif (char in symbols):
            
            if (len(code) > i + 2) and (char + code[i + 1] + code[i + 2]) in (symbols) and (triple_operator is False):
                # Build token
                current_token += char
                triple_operator = not triple_operator
                continue

            elif triple_operator:
                if (len(current_token) < 2):
                    current_token += char
                    continue

                current_token += char
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                triple_operator = not triple_operator
            
            elif (char + code[i + 1]) in symbols and (double_operator is False) and (triple_operator is False):
                # Build token
                current_token += char
                double_operator = not double_operator
                continue
            
            elif double_operator:
                # Get the index of char in the double operators list
                current_token += char
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                double_operator = not double_operator
            
            else:
                # Get the index of char in the single operators list
                current_token += char
                lexemes.append(char)
                lexemes_display.append(char)

            # Implement exception handling for when ValueError is encountered
            try:
                # Use the index to access the corresponding token description
                index = symbols.index(current_token)
                token_description = TT_Operators[index][1]
                tokens_display.append(token_description)
                current_token = ''

            except ValueError:
                tokens_display.append("ERROR: Invalid Token")

        # Check for invalid tokens
        # This part of the lexical for digit when identifying an identifier with number as the start
        # This is to skip the remaining char for an identifier with number as the start
        elif char in invalid_token:
            invalid_token = invalid_token[1:]
            continue

        #KEYWORDS AND IDENTIFIER

        # Checks if the char is alphabet, _, or a digit 
        # accepts the digit only if the current token is not empty meaning there is a word before the number
        # and when the current token is not all digits(need kasi na pag digits sa number sha)
        elif char.isalpha() or char == '_' or (char.isdigit() and current_token != '' and not current_token.isdigit() and '.' not in current_token):
            # The character is alphabetical, _, add it to the current token
            current_token += char
            if (i + 1 < len(code)) and (not code[i + 1].isalnum() and code[i + 1] != '_'):
                # Check if the current token is a data type keywordnot(code[i + 1].isalpha()):
                lexemes.append(current_token)
                lexemes_display.append(current_token)

                if current_token in datatype:
                    tokens_display.append("Data Type Keyword")

                elif current_token in controlflow:
                    tokens_display.append("Control Flow Keyword")

                elif current_token in storageclass:
                    tokens_display.append("Storage Class Keyword")

                elif current_token in otherkeywords:
                    tokens_display.append("Other Keywords")

                else:
                    tokens_display.append("Identifier")
                
                current_token = ''

            else: continue
        
        # Check if input is a numeric constant
        elif char in digits or char == '.':
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
                lexemes_display.append(current_token)
                tokens_display.append("ERROR: Invalid Token")

                # eto yung invalid token sa taas, pinasa sha para lagpasan na lang yung part pa nung identifier
                invalid_token = current_token
                invalid_token = invalid_token[1:]
                current_token = ''
            
            elif (i + 1 < len(code)) and (not code[i + 1] in digits and '.' in current_token):
                lexemes[-1] = current_token
                lexemes_display[-1] = current_token
                tokens_display[-1] = ("Float-Point Constant")
                current_token = ''

            #pa add na lang ako here paano yung sa float
            elif (i + 1 < len(code)) and (not code[i + 1] in digits and code[i + 1] != '.'):
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                tokens_display.append("Integer Constant")
                current_token = ''

        else:
            lexemes.append(char)
            lexemes_display.append(char)
            tokens_display.append("ERROR: Invalid Token")
            current_token = ''
    
    return lexemes_display, tokens_display
