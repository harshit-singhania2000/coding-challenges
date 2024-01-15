def check_parse_successfull(func):
    def wrapper(input_str):
        try:
            res = func(input_str)
        except Exception as e:
            return None, input_str
        return res
    return wrapper

@check_parse_successfull
def parse_string(input_str):
    result = ""
    assert input_str[0] == "\"", "no start quote found"
    input_str = input_str[1:]
    for i, char in enumerate(input_str):
        if char == "\"":
            return result, input_str[i+1:]
        result += char
    raise Exception("no end quotes found")

@check_parse_successfull
def parse_number(input_str):
    result = ""
    digits = "0123456789"
    terminators = ":, }]"
    if input_str[0] == "-":
        result += "-"
        input_str = input_str[1:]
    for i, char in enumerate(input_str):
        if char in digits or char == ".":
            result += char
        elif char in terminators:
            return float(result), input_str[i:]
        else:
            raise Exception("invalid character found %s"%char)
    return float(result), ""

@check_parse_successfull
def parse_whitespace(input_str):
    if input_str=="":
        return "", ""
    return "", input_str.lstrip().lstrip("\n")    
    
@check_parse_successfull
def parse_value(input_str):
    _, input_str = parse_whitespace(input_str)
    for parse_func in [parse_string, parse_number, parse_array, parse_object]:
        parsed_val, remaining_str = parse_func(input_str)
        if parsed_val is not None:
            _, remaining_str = parse_whitespace(remaining_str)
            return parsed_val, remaining_str
    raise Exception("this is not an appropriate value")

@check_parse_successfull
def parse_array(input_str):
    assert input_str[0] == "[", "no start bracket found"
    input_str = input_str[1:]
    result = []
    while True:
        _, input_str = parse_whitespace(input_str)
        if input_str[0] == "]":
            return result, input_str[1:]
        value, remaining_str = parse_value(input_str)
        if value is None:
            raise Exception("can't parse, invalid value %s", input_str)
        input_str = remaining_str
        result.append(value)
        if input_str[0] == ",":
            input_str = input_str[1:]

@check_parse_successfull
def parse_object(input_str):
    assert input_str[0] == "{", "no start bracket found"
    input_str = input_str[1:]
    result = {}
    while True:
        _, input_str = parse_whitespace(input_str)
        if input_str[0] == "}":
            return result, input_str[1:]
        key, remaining_str = parse_string(input_str)        
        if key is None:
            raise Exception("can't parse, invalid value for key %s", input_str)        
        input_str = remaining_str
        _, input_str = parse_whitespace(input_str)
        assert input_str[0] == ":", "expected : but didnt find it here: %s"%input_str
        input_str = input_str[1:]        
        value, remaining_str = parse_value(input_str)   
        if value is None:
            raise Exception("can't parse, invalid value %s", input_str)        
        result.update({key: value})
        input_str = remaining_str
        if input_str[0] == ",":
            input_str = input_str[1:]

def parse(json_string):
    parsed_value, remaining_str = parse_value(json_string)
    return parsed_value

if __name__ == "__main__":
    # a few test cases
    print(parse("\"abc\""))
    print(parse("0.123"))
    print(parse("1.23"))
    print(parse("[1.2, 2.1, 3.5]"))
    print(parse("[\"abcd\", \"def\", 1.2]"))
    print(parse("[[1,2],[3,4],[\"abc\", \"def\"]]"))
    print(parse("[[1,2],[3,4],[\"abc\", \"def\"]]"))
    print(parse("{\"a\": 1}"))
    print(parse("{\"a\": [1,2,3]}"))