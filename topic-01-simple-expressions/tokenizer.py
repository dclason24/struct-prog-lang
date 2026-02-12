import re
from pprint import pprint

# p = re.compile("ab*")

# if p.match("abbbbbbb") :
#     print("match")
# else:
#     print("not match")

# if something looks like this, label it as this
# "." matches any character, so if nothing else matched, its invalid 
#and it throws an error

 #r means regular expression - just signifies we are making a r expression
patterns = [
    (r"\s+", "whitespace"),
    (r"\d+", "number"),
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\*", "*"),
    (r"\(", "("),
    (r"\)", ")"),
  #added this line beneath
    (r"%", "%"),
    (r".", "error"),
]

patterns = [(re.compile(p), tag) for p, tag in patterns]


def tokenize(characters):
    "Tokenize a string using the patterns above"
    #tokens collected
    tokens = []
    #cuurent position
    position = 0
    #these 2 are used for error reporting
    line = 1
    column = 1
    current_tag = None

#until the end of the input
    while position < len(characters):
        #loop through all the patterns
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            #if they match, stop checking and break
            if match:
                current_tag = tag
                break
        assert match is not None
        //what are the characters that match this pattern?
        value = match.group(0)

        # there was an invalid character in there
        #look at the tag that was left behind
        if current_tag == "error":
            raise Exception(f"Unexpected character: {value!r}")

        #skipping whitespace
        if tag != "whitespace":
            token = {"tag": current_tag, "line": line, "column": column}
            #if the tag is a number it converts it to an integer
            if current_tag == "number":
                token["value"] = int(value)
            #adds it to the other tokens
            tokens.append(token)

        # advance position and update line/column
        for ch in value:
            if ch == "\n":
                line += 1
                column = 1
            else:
                column += 1
        position = match.end()

    #this is a special end of file token to know when to stop
    tokens.append({"tag": None, "line": line, "column": column})
    return tokens


def test_digits():
    print("test tokenize digits")
    t = tokenize("123")
    assert t[0]["tag"] == "number"
    assert t[0]["value"] == 123
    assert t[1]["tag"] is None
    t = tokenize("1")
    assert t[0]["tag"] == "number"
    assert t[0]["value"] == 1
    assert t[1]["tag"] is None


def test_operators():
    print("test tokenize operators")
    t = tokenize("+ - * / ( ) %")
    tags = [tok["tag"] for tok in t]
    assert tags == ["+", "-", "*", "/", "(", ")", "%", None]


def test_expressions():
    print("test tokenize expressions")
    t = tokenize("1+222*3")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 222
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] is None


def test_whitespace():
    print("test tokenize whitespace")
    t = tokenize("1 +\t2  \n*    3")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 2
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] is None


def test_error():
    print("test tokenize error")
    try:
        t = tokenize("1@@@ +\t2  \n*    3")
    except Exception as e:
        assert str(e) == "Unexpected character: '@'"
        return
    assert Exception("Error did not happen.")


if __name__ == "__main__":
    test_digits()
    test_operators()
    test_expressions()
    test_whitespace()
    test_error()
    print("done.")
