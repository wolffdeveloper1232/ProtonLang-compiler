# compiler for proton lang
# out = print
# use var: when setting a var, and also add ; to the end of that line
# there must be no commands before }

def count_nostr(string, thing):
        instring = False
        
        out = 0
        
        for i in string:
            if i == '"':
                instring = not instring

            if instring:
                continue

            if i == thing:
                out += 1

        return out

def _in(string):
    if string != "in:":
        return string

    return "input()"

code = """
var: user = in: ;
var: counter = 0 ;
loop{
    out(user)
    inc: counter;
    same counter 5 {
        stop:
    }
}

"""
codepy = ""

depth = 0

def setup():
    global var, varset, same, same2, instring, dec, inc
    var = False
    varset = False
    same = False
    same2 = False # second part of same
    instring = False # this one is not used for a segment, but rather to make sure the () does not break
    dec = False
    inc = False

for line in code.split("\n"):
    line = line.strip()
    setup()
    if line == '':
        continue
    token = ""

    depth -= count_nostr(line, "}")
    codepy += " " * depth
    depth += count_nostr(line, "{")

    if depth < 0:
        raise Exception("Error: depth is negative, reason is probably too many }")
        
    for char in line:
        token += char
        if char == '"':
            instring = not instring
            
        # if its a var
        if var:
            if token.endswith(" "):
                token = token[0:len(token)-1]
            if ( token.endswith("=") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.strip().replace(";","")
                if token.endswith("="):
                    varset = True
                
                token = ""
                var = False
            continue
            
        # if its setting a var
        if varset:
            if token == " ":
                token = ""
            if token.endswith(";"):
                codepy += _in(token.replace(";", "").strip())
                token = ""
                varset = False
            continue
                
        # if its "same"
        if same:
            if token == " ":
                token = ""
            if token.endswith(" ") and not instring:
                codepy += token.strip() + "=="
                token = ""
                same = False
                same2 = True
            continue

        # second part
        if same2:
            if token == " ":
                token = ""
            if ( token.endswith(" ") or token.endswith("{") ) and not instring:
                codepy += token.strip().replace("{","")+":"
                token = ""
                same2 = False

        # if dec
        if dec:
            if token == " ":
                token == ""
            if ( token.endswith(" ") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.strip().replace(";","") + "-=1"
                token == ""
                dec = False

        # if inc
        if inc:
            if token == " ":
                token == ""
            if ( token.endswith(" ") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.strip().replace(";","") + "+=1"
                token == ""
                inc = False
            
        # normal stuff:
        if token == "}":
            token = ""
        elif token == "{":  
            token = ""
        elif token.strip() == "out":
            codepy += "print"
            token = ""
        elif token.replace(" ","").startswith('(') and token.endswith(')') and not instring:
            codepy += token.strip()
            token = ""
        elif token == "var:":
            var = True
            token = ""
        elif token == "same ":
            same = True
            token = ""
            codepy += "if "
        elif token == " ":
            token = ""
        elif token == "else " or token == "else{":
            token = ""
            codepy += "else:"
        elif token == "stop:":
            token = ""
            codepy += "break"
        elif token == "loop" or token == "loop{":
            token = ""
            codepy += "while True:"
        elif token == "dec:":
            token = ""
            dec = True
        elif token == "inc:":
            token = ""
            inc = True
            
    codepy += "\n"
    if var:
        raise Exception("Error: used var keyword without a var after")
    if same or same2:
        raise Exception("Error: incomplete same statement")
    if instring:
        raise Exception("Error: you didnt complete the string. FINISH IT.")
    
print(codepy) # using exec for testing purposes 
