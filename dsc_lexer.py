from tokentypes import TT_Operators, TT_ControlFlowKeywords, TT_DataTypeKeywords, TT_StorageClassKeywords, TT_OtherKeywords, TT_Delimiters
from tokentypes import alphabet, digits, noise_words
    
def lexical_analyzer(code):
    lexemes = []
    lexemes_display = []
    tokens_display = []
    line_count_list = []   
    current_token = ''
    invalid_token = ''
    string_delimiter_count = 0
    in_singlecomment = False
    in_multiplecomment = False
    in_string = False
    period_count = 0
    line_count = 1
     
    symbols = [symbol for symbol, _ in TT_Operators] 
    delims = [symbol for symbol, _ in TT_Delimiters]   
    controlflow = list(TT_ControlFlowKeywords)
    datatype = list(TT_DataTypeKeywords)
    storageclass = list(TT_StorageClassKeywords)
    otherkeywords = list(TT_OtherKeywords)

    
    # Iterate through each character in the code
    for i in range(len(code)):
        char = code[i]

        # LINES
        if code[i] == "\n":
            line_count += 1

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
            tokens_display.append("COMMENT")
            line_count_list.append(str(line_count))
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
            tokens_display.append("COMMENTS")
            line_count_list.append(str(line_count))
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
                lexemes.append(string_char)
                lexemes_display.append(string_char)
                line_count_list.append(str(line_count))

            # If encounters a closing delimiter, close the string input
            elif string_delimiter_count == 2:
                lexemes[-1] = current_token
                string_delimiter_count = 0

                # Check if string is a string literal
                if (string_char == char) and (string_char == '"'):
                    string_display = current_token[1 : -1]
                    lexemes_display[-1] = string_char + string_display[:9] + '...' + char
                    tokens_display[-1] = "STRING_CONSTANT"

                # Check if string uses single quotes delimiter
                elif (string_char == char) and (string_char == "'"):
                    # If the input is a single character
                    if len(current_token) == 3:
                        lexemes_display[-1] = current_token
                        tokens_display[-1] = "CHARACTER_CONSTANT"
                    
                    # Else, notify wrong delimiter used
                    else:
                        tokens_display[-1] = "ERROR: Character Literal Delimiter Used for String Literal"

                # Notify different string delimiters employed
                else:
                    tokens_display[-1] = "ERROR: Different String Delimiters Employed"
                
                current_token = ''
                line_count_list[-1] = str(line_count)
        
        # While in_string is true, all following inputs will count as part of the String Constant
        elif in_string:
            current_token += char

            # Format for string display in GUI
            if len(current_token) < 14:
                lexemes_display[-1] = current_token[:10] + "..."
        
        #KEYWORDS AND IDENTIFIER
        # Check for invalid tokens to skip the remaining character for an identifier starting with a digit
        elif char in invalid_token:
            invalid_token = invalid_token[1:]
            continue
        
        # Checks if the character is an alphabet, _, or a digit 
        # Accepts the digit only if the current token is not empty meaning there is a word before the number
        elif char in alphabet or char == '_' or (char.isdigit() and current_token != '' and not current_token.isdigit() and '.' not in current_token):
            current_token += char
            
            if (i + 1 < len(code)) and (not ((code[i + 1] in alphabet) or (code[i + 1] in digits))  and code[i + 1] != '_'):
                # Check if the current token is a keyword
                lexemes.append(current_token)
                lexemes_display.append(current_token)

                if current_token in datatype:
                    for j in range(len(noise_words)):
                        noise_word = noise_words[j]
                        if noise_word in current_token:
                            current_token = current_token.replace(noise_word, '')
                            lexemes[-1] = current_token
                            lexemes_display[-1] = current_token
                            line_count_list[-1] = str(line_count)
                    tokens_display.append("DATATYPE_KW")

                elif current_token in controlflow:
                    tokens_display.append("CTRLFLOW_KW")

                elif current_token in storageclass:
                    tokens_display.append("STRGCLSS_KW")

                elif current_token in otherkeywords:
                    tokens_display.append("KEYWORD")

                else:
                    tokens_display.append("IDENTIFIER")
                
                current_token = ''
                line_count_list.append(str(line_count))

            else: continue
        
        # NUMERICAL CONSTANTS
        # Check if input is a digit
        elif char in digits or char == '.':
            current_token += char
            
            # Check if character is a period
            if char == '.':
                period_count += 1

            # Check if the digit is followed by an alphabet or _ (Invalid Identifier)
            if (i + 1 < len(code)) and (code[i + 1] in alphabet or code[i + 1]=='_'):
                j = i
                
                # Iterate all the characters of the the invalid identifiers
                while ((code[j + 1] in alphabet) or (code[j + 1] in digits) or code[j + 1]=='_'):
                    current_token += code[j + 1]
                    j+=1
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                tokens_display.append("ERROR: Invalid Identifier")
                line_count_list.append(str(line_count))

                # Used for handling the invalid identifier
                invalid_token = current_token
                invalid_token = invalid_token[1:]
                current_token = ''

            #Check if the following character is a digit or period
            elif (i + 1 < len(code)) and (code[i + 1] in digits or code[i + 1] == '.'):
                continue

            else:
                # Check if input is a integer constant
                if period_count == 0:
                    lexemes.append(current_token)
                    lexemes_display.append(current_token)
                    tokens_display.append("INT_CONST")
                    line_count_list.append(str(line_count))
                    current_token = ''
                
                # Check if input is a floating-point constant
                elif period_count == 1:
                    lexemes.append(current_token)
                    lexemes_display.append(current_token)
                    tokens_display.append("FLOAT_CONST")
                    line_count_list.append(str(line_count))
                    current_token = ''
                    period_count = 0

                else:
                    lexemes.append(current_token)
                    lexemes_display.append(current_token)
                    tokens_display.append("ERROR: Invalid Token")
                    line_count_list.append(str(line_count))
                    period_count = 0
                    current_token = ''
                
        # OPERATORS AND SPECIAL SYMBOLS
        # Check if input is a operator or special symbol
        elif (char in symbols or char in delims):
            current_token += char

            # Check if the next character is in symbols
            if code[i + 1] in symbols:
                continue

            elif char in delims:
                lexemes.append(current_token)
                lexemes_display.append(current_token)
                index = delims.index(current_token)
                token_description = TT_Delimiters[index][1]
                tokens_display.append(token_description)
                line_count_list.append(str(line_count))
                current_token = ''
                
            
            # Check if the string of symbols is in the list
            else:
                try:
                    # Use the index to access the corresponding token description
                    lexemes.append(current_token)
                    lexemes_display.append(current_token)
                    index = symbols.index(current_token)
                    token_description = TT_Operators[index][1]
                    tokens_display.append(token_description)
                    line_count_list.append(str(line_count))
                    current_token = ''

                except ValueError:
                    tokens_display.append("ERROR: Invalid Token")
                    line_count_list.append(str(line_count))
                    current_token = ''

        # INVALID TOKENS
        # If the input did not fit on any of the if condition, consider as an Invalid Token
        else:
            lexemes.append(char)
            lexemes_display.append(char)
            tokens_display.append("ERROR: Invalid Token")
            line_count_list.append(str(line_count))
            current_token = ''
    
    return lexemes, lexemes_display, tokens_display, line_count_list
