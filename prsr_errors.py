# Error for missing semicolon
def error_missing_semicolon(lines, value, result, after_token):
    lines.append(value)
    result.append("Expected semicolon ';' after " + after_token)
    return

def error_expected_after(lines, value, result, expected_token, after_token):
    lines.append(value)
    result.append("Expected " + expected_token + " after " + after_token)
    return