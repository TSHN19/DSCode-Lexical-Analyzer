from prsr_errors import error_invalid_syntax, error_expected_after, error_missing_semicolon
from prsr_otherfunctions import pop_first_element

def parse_otherkeywords(number_line, tokens, lexemes, lines, result, Node):
    if lexemes[0] == "print":
        return parse_print(number_line, tokens, lexemes, lines, result, Node)
    
    # Add elif for keywords na under ng otherkeywords

# Create new function per keywords

# Print Keyword
def parse_print(number_line, tokens, lexemes, lines, result, Node):
    popped_print = pop_first_element(number_line, tokens, lexemes)

    # Check if print keyword is followed by left parenthesis
    if tokens and tokens[0] == "LPAREN":
        popped_lparen = pop_first_element(number_line, tokens, lexemes)
        argument = print_argument(number_line, tokens, lexemes, lines, result, Node)

        # Check if left parenthesis is followed by a print argument
        if argument[0]:

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
                    node = Node("", [])
                    error_missing_semicolon(lines, popped_rparen[1], result, "')'")
                    return node, lines, result
            
            # Error for missing right parenthesis
            else:
                node = Node("", [])
                error_expected_after(lines, popped_lparen[1], result, "')'", "print argument")
                return node, lines, result
        
        # Error for missing print argument
        else:
            node = Node("", [])
            error_expected_after(lines, popped_lparen[1], result, "print argument", "'('")
            return node, lines, result

    # Error for inavlid syntax   
    else:
        node = Node("", [])
        error_invalid_syntax(lines, popped_print[1], result, "Print")
        return node, lines, result

def print_argument(number_line, tokens, lexemes, lines, result, Node):
    return # Gagawa ng para maghandle nung arguments sa print: identifiers, string, expressions (kung ano tinatanggap ng printf sa C)