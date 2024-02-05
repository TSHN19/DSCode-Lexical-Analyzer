def pop_first_element(number_line, tokens, lexemes):
    tokens_value = tokens.pop(0)
    lexemes.pop(0)
    number_line_value = number_line.pop(0)
    return tokens_value, number_line_value