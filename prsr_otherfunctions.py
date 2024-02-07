def pop_first_element(number_line, tokens, lexemes):
    tokens_value = tokens.pop(0)
    number_line_value = number_line.pop(0)
    lexemes_value = lexemes.pop(0)
    return tokens_value, number_line_value, lexemes_value

def check_for_error(node, Node):
    if node.value == "Error":
        return True
    else:
        # If it's not an error or a leaf node, recursively check its children
        for child in node.children:
            if check_for_error(child):
                return True
        return False
