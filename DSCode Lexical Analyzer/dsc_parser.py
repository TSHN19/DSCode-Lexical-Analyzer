def syntax_analyzer(tokens, number_line):
    invalid_token = "ERROR"
    parser_result = []
    parser_lines = []


    for i in range(len(tokens)):
        current_token = tokens[i]
        current_line = number_line[i]

        if invalid_token in current_token:
            parser_result.append("Invalid Token")
            parser_lines.append(current_line)

    return parser_lines, parser_result