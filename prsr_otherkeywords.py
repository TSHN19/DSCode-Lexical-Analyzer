from prsr_errors import error_invalid_syntax, error_expected_after, error_missing_semicolon
from prsr_otherfunctions import pop_first_element

def parse_otherkeywords(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "print":
        return parse_print(number_line, tokens, lexemes, lines, result, Node)
    elif lexemes[0] == "const":
        return parse_const(number_line, tokens, lexemes, lines, result, Node)
    elif lexemes[0] == "input":
        return parse_input(number_line, tokens, lexemes, lines, result, Node)

# Const Keyword
def parse_const(number_line, tokens, lexemes, lines, result, Node):
    popped_const = pop_first_element(number_line, tokens, lexemes)
    
     # Check if const is followed by a datatype
    if tokens and tokens[0] == "DATATYPE_KW":
        popped_datatype = pop_first_element(number_line, tokens, lexemes)
        datatype = Node("DataType", [popped_datatype[2]])

        # Check if data type is followed by an identifier
        if tokens and tokens[0] == "IDENTIFIER":
            popped_identifier = pop_first_element(number_line, tokens, lexemes)
            identifier = Node("Identifier", [popped_identifier[2]])
            
            # If identifier is followed by a semicolon
            if tokens and tokens[0] == "SEMICOLON":
                node = Node("Const", [datatype, identifier])
                popped_semicolon = pop_first_element(number_line, tokens, lexemes)
                return node, popped_semicolon[1], result
            
            # Error if missing semicolon
            else:
                node = Node("Const", [datatype, identifier, Node("Error", [])])
                error_expected_after(lines, popped_identifier[1], result, "Data Type", "Const")
                return node, popped_identifier[1], result
            
        # Error if missing identifier
        else:
            node = Node("Const", [datatype, Node("Error", [])])
            error_expected_after(lines, popped_datatype[1], result, "Data Type", "Const")
            return node, popped_datatype[1], result

    # Error if const is not followed by a datatype 
    else:
        node = Node("Const", [Node("Error", [])])
        error_expected_after(lines, popped_const[1], result, "Data Type", "Const")
        return node, popped_const[1], result
    
#Input Keyword
def parse_input(number_line, tokens, lexemes, lines, result, Node):
    popped_input = pop_first_element(number_line, tokens, lexemes)

    # Check if inputt keyword is followed by left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        
        if tokens:
            argument = input_argument(number_line, tokens, lexemes, lines, result, Node)

            # Check if left parenthesis is followed by an input argument
            if argument[0]!= None:

                # Check if input argument is followed by right parenthesis
                if tokens and tokens[0] == "RPAREN":
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)

                    # Check if statement ends in semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Input", [argument])
                        pop_first_element(number_line, tokens, lexemes)
                        return node, lines, result
                    
                    # Error for missing semicolon
                    else:
                        node = None
                        error_missing_semicolon(lines, popped_rparen[1], result, "')'")
                        return node, lines, result
                
                # Error for missing right parenthesis
                else:
                    node = None
                    error_expected_after(lines, popped_lparen[1], result, "')'", "input argument")
                    return node, lines, result
            
            # Error for missing input argument
            else:
                node = None
                return node, lines, result
        else:
            node = None
            error_expected_after(lines, popped_lparen[1], result, "identifier", "'('")
            return node, lines, result    

    # Error for inavlid syntax   
    else:
        node = None
        error_expected_after(lines, popped_input[1], result, "'('", "input keyword")
        return node, lines, result
    
 
def input_argument(number_line, tokens, lexemes, lines, result, Node):
    arguments = []
    
    while tokens and tokens[0] != "RPAREN":
        if tokens and tokens[0] == "IDENTIFIER":
            argument_content = pop_first_element(number_line, tokens, lexemes)

        else:
            argument_content = pop_first_element(number_line, tokens, lexemes)
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "identifier", "input argument")
            return node, argument_content[1], result
    
        arguments.append(argument_content)
        if tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
        elif tokens and tokens[0] == "RPAREN":
            break
        else:
            node = None
            error_expected_after(lines, argument_content[1], result, "',' or ')'", argument_content[2])
            return node, lines, result
        
    if tokens:
        if tokens and tokens[0] == "RPAREN":
            node = [Node("Arguments", [id]) for id in arguments]
            return node, lines, result
    else:
        node = None
        error_expected_after(lines, argument_content[1], result, "identifier", "'" + argument_content[2] + "'")
        return node, lines, result 


# Print Keyword
def parse_print(number_line, tokens, lexemes, lines, result, Node):
    popped_print = pop_first_element(number_line, tokens, lexemes)

    # Check if print keyword is followed by left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)

        if tokens:
            argument = print_argument(number_line, tokens, lexemes, lines, result, Node)

            # Check if left parenthesis is followed by a print argument
            if argument[0] != None:

                # Check if print argument is followed by righ parenthesis
                if tokens and tokens[0] == "RPAREN":
                    popped_rparen = pop_first_element(number_line, tokens, lexemes)

                    # Check if statement ends in semicolon
                    if tokens and tokens[0] == "SEMICOLON":
                        node = Node("Print", [argument])
                        pop_first_element(number_line, tokens, lexemes)
                        return node, lines, result
                    
                    # Error for missing semicolon
                    else:
                        node = None
                        error_missing_semicolon(lines, popped_rparen[1], result, "')'")
                        return node, lines, result
                
                # Error for missing right parenthesis
                else:
                    node = None
                    error_expected_after(lines, popped_lparen[1], result, "')'", "print argument")
                    return node, lines, result
            
            # Error for missing print argument
            else:
                node = None
                return node, lines, result
        else:
            node = None
            error_expected_after(lines, popped_lparen[1], result, "string literal or identifier", "'('")
            return node, lines, result

    # Error for inavlid syntax   
    else:
        node = None
        error_expected_after(lines, popped_print[1], result, "'('", "print keyword")
        return node, lines, result

def print_argument(number_line, tokens, lexemes, lines, result, Node):
    arguments = []
    
    while tokens and tokens[0] != "RPAREN":
        if tokens and tokens[0] == "STRING_CONSTANT":
            argument_content = pop_first_element(number_line, tokens, lexemes)
            
        elif tokens and tokens[0] == "IDENTIFIER":
            argument_content = pop_first_element(number_line, tokens, lexemes)

        else:
            argument_content = pop_first_element(number_line, tokens, lexemes)
            node = [Node("Arguments", [id]) for id in arguments]
            error_expected_after(lines, argument_content[1], result, "string literal or identifier", "print argument")
            return node, argument_content[1], result
    
        arguments.append(argument_content)
        if tokens and tokens[0] == "COMMA":
            pop_first_element(number_line, tokens, lexemes)
        elif tokens and tokens[0] == "RPAREN":
            break
        else:
            node = None
            error_expected_after(lines, argument_content[1], result, "',' or ')'", argument_content[2])
            return node, lines, result
        
    if tokens:
        if tokens and tokens[0] == "RPAREN":
            node = [Node("Arguments", [id]) for id in arguments]
            return node, lines, result
    else:
        node = None
        error_expected_after(lines, argument_content[1], result, "string literal or identifier", "'" + argument_content[2] + "'")
        return node, lines, result 
        