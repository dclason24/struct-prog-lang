import re

patterns = [
  //r means regular expression - just signifies we are making a r expression
  (r"\s+", "whitespace"),
  (r "\d+", "number"),
  (r "\+", "+"),
  (r"\-", "-"),
  (r "\/", "/"),
  (r "\*", "*"),
  (r ".", "error")
]


patterns = [(re.compile(p), tag) for p, tag in patterns]

def tokenize(characters):
  "tokenize a string using the patterns above"
  tokens = []
  position = 0
  line = 1
  column = 1
  current_tag = None

  while position < len(characters):
    for pattern, tag in patterns:
      match = pattern.match(characters, position)
      if match:
        break
    assert match it not None
    //what are the characters that match this pattern?
    value = match.group(0)

    //look at the tag that was left behind
        if current_tag == "error"
            raise Exception(f"Unexpected character: {value!r}")
    
        if tag != "whitespace":
            token = {"tag": current_tag, "line": line, "column": column}
        if current_tag = "number":
            token["value] = int(value)
            tokens.append(token)

