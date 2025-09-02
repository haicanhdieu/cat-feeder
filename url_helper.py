def url_decode(s):
    s = s.replace('+', ' ')
    result = ""
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            try:
                result += chr(int(s[i+1:i+3], 16))
                i += 3
            except ValueError:
                result += s[i]
                i += 1
        else:
            result += s[i]
            i += 1
    return result
