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

        # COMMENTS
        # Check if the current and succeeding character has a single-line comment symbol
        if char == "/" and code[i + 1] == "/":
            current_token += char
            in_singlecomment = not in_singlecomment

        # If single-line comment is True, all inputs will count as a comment unless a newline is encountered
        elif in_singlecomment and char == "\n":
            in_singlecomment = not in_singlecomment
            lexemes.append(current_token)
            lexemes_display.append(current_token)
            tokens_display.append("Single-Line Comment")
            current_token = ''

        # Check if the current and succeeding character has a multiple comment symbol
        elif char == "/" and code[i + 1] == "*":
            current_token += char
            in_multiplecomment = not in_multiplecomment

        # If multiple-line comment is True, check if the current and succeeding character has the closing multiple-comment symbol
        elif in_multiplecomment and code[i - 1] == "*" and char == "/":
            current_token += char
            in_multiplecomment = not in_multiplecomment
            lexemes.append(current_token)
            lexemes_display.append(current_token)
            tokens_display.append("Multiple-Line Comment")
            current_token = ''
        
        # If single-line or multiple-line comment is True, build the comment through the inputs
        elif in_singlecomment or in_multiplecomment:
            current_token += char

        # BLANKS
        # Check if the character is a blank, and not inside a string or comments
        elif ((char == ' ') or (char == '\n') or (char == '\t')) and not(in_string or in_singlecomment or in_multiplecomment):
            continue
        
        # STRING AND CHARACTER CONSTANT
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
        
        # While in_string is true, all following inputs will count as part of the String Constant
        elif in_string:
            current_token += char

            # Format for string display in GUI
            if len(current_token) < 14:
                lexemes_display[-1] = current_token[:10] + "...?"

        # OPERATORS AND SPECIAL SYMBOLS
        # Check if input is a operator or special symbol
        elif (char in symbols):
            
            # Check if the current character is part of a triple operator
            if (len(code) > i + 2) and (char + code[i + 1] + code[i + 2]) in (symbols) and (triple_operator is False):
                current_token += char
                triple_operator = not triple_operator
                continue
            
            # Iterate through the next two characters of the triple operator
            elif triple_operator:
                if (len(current_token) < 2):
                    current_token += char
                    continue

                current_token += char
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                triple_operator = not triple_operator
            
            # Check if the current character is part of a double operator
            elif (char + code[i + 1]) in symbols and (double_operator is False) and (triple_operator is False):
                current_token += char
                double_operator = not double_operator
                continue
            
            # Iterate through the next two characters of the double operator
            elif double_operator:
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

        
        
        #KEYWORDS AND IDENTIFIER
        # Check for invalid tokens to skip the remaining character for an identifier starting with a digit
        elif char in invalid_token:
            invalid_token = invalid_token[1:]
            continue
        
        # Checks if the character is an alphabet, _, or a digit 
        # Accepts the digit only if the current token is not empty meaning there is a word before the number
        elif char.isalpha() or char == '_' or (char.isdigit() and current_token != '' and not current_token.isdigit() and '.' not in current_token):
            current_token += char
            if (i + 1 < len(code)) and (not code[i + 1].isalnum() and code[i + 1] != '_'):
                
                # Check if the current token is a keyword
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
        
        # NUMERICAL CONSTANTS
        # Check if input is a digit
        elif char in digits or char == '.':
            current_token += char
            
            # Check if the digit is followed by an alphabet or _ (Invalid Identifier)
            if (i + 1 < len(code)) and (code[i + 1].isalpha() or code[i + 1]=='_'):
                j = i
                
                # Iterate all the characters of the the invalid identifiers
                while (code[j + 1].isalnum() or code[j + 1]=='_'):
                    current_token += code[j + 1]
                    j+=1
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                tokens_display.append("ERROR: Invalid Token")

                # Used for handling the invalid identifier
                invalid_token = current_token
                invalid_token = invalid_token[1:]
                current_token = ''
            
            # Check if input is a floating-point constant
            elif (i + 1 < len(code)) and (not code[i + 1] in digits and '.' in current_token):
                lexemes[-1] = current_token
                lexemes_display[-1] = current_token
                tokens_display[-1] = ("Float-Point Constant")
                current_token = ''

            # Check if input is a integer constant
            elif (i + 1 < len(code)) and (not code[i + 1] in digits and code[i + 1] != '.'):
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                tokens_display.append("Integer Constant")
                current_token = ''

        # INVALID TOKENS
        # If the input did not fit on any of the if condition, consider as an Invalid Token
        else:
            lexemes.append(char)
            lexemes_display.append(char)
            tokens_display.append("ERROR: Invalid Token")
            current_token = ''
    
    return lexemes_display, tokens_display
