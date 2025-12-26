# compiler for proton lang
# out = print
# use var: when setting a var, and also add ; to the end of that line
# there must be no commands before }

def count_nostr(string, thing):
        instring = False
        
        out = 0
        
        for i in range(len(string)):
            if string[i:i+len(thing)] == '"':
                instring = not instring

            if instring:
                continue

            if string[i:i+len(thing)] == thing:
                out += 1

        return out

def _in(string):
    if string != "in:":
        return string

    return "input()"

# if you want to get stuff from the table, use gettable(table, index)
code = """
var: user = in: ;
table: stuff {
    user;
}
out(gettable(stuff, 1))
"""

codepy = ""

# make functions for things i dont feel like compiling only if needed:
if count_nostr(code, "table:"):
    codepy += """def gettable(table, index):
 return eval(f"table.e{index}")
"""

depth = 0

def setup():
    global var, varset, same, same2, instring, dec, inc, table, comment
    var = False
    varset = False
    same = False
    same2 = False # second part of same
    instring = False # this one is not used for a segment, but rather to make sure the () does not break
    dec = False
    inc = False
    table = False
    comment = False # this one is not used for a segment.

setup()
table2 = False
counter = 0
for line in code.split("\n"):
    line = line.strip()
    # setup()
    comment = False
    if line == '':
        continue

    if table2:
        counter += 1
            
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
        elif char == "#" and not instring:
            comment = True
            break
            
        # if its a var
        if var:
            if token.endswith(" "):
                token = token[0:len(token)-1]
            if ( token.endswith("=") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.replace(";","").strip()
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
                codepy += token.replace("{","").strip()+":"
                token = ""
                same2 = False
            continue

        # if dec
        if dec:
            if token == " ":
                token == ""
            if ( token.endswith(" ") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.replace(";","").strip() + "-=1"
                token == ""
                dec = False
            continue

        # if inc
        if inc:
            if token == " ":
                token == ""
            if ( token.endswith(" ") or token.endswith(";") ) and len(token) > token.count(" "):
                codepy += token.strip().replace(";","") + "+=1"
                token == ""
                inc = False
            continue

        # if its a table
        if table:
            if token == " ":
                token = ""
            token = token.strip()
            if ( token.endswith(" ") or token.endswith("{") ) and len(token) > token.count(" "):
                codepy += f'class {token.replace("{","")}:'
                tablename = token.replace("{","")
                codepy += "\n def __init__(self):"
                token = ""
                table = False
                table2 = True
            continue

        # second part
        if table2:
            if line == '':
                continue
            if token == " ":
                token == ""
            if token.endswith(";") and len(token) > token.count(" "):
                codepy += f" self.e{str(counter)}=" + token.replace(";","").strip()
            if char == "}":
                codepy += f"{tablename} = {tablename}()"
                counter = 0
                table2 = False
            continue
            
            
        # normal stuff:
        if token == "}":
            token = ""
        elif token == "{":  
            token = ""
        elif token.strip() == "out":
            codepy += "print"
            token = ""
        elif token.replace(" ","").startswith('(') and token.endswith(')') and (not instring) and count_nostr(token, "(") == count_nostr(token, ")"):
            codepy += token.strip()
            token = ""
        elif token == "var:":
            var = True
            token = ""
        elif token == "same ":
            same = True
            token = ""
            codepy += "if "
        elif token == " " and not instring:
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
        elif token == "table:":
            token = ""
            table = True
            
    if not comment:
        codepy += "\n"
    else:
        setup()
    if var:
        raise Exception("Error: used var keyword without a var after")
    if same or same2:
        raise Exception("Error: incomplete same statement")
    if instring:
        raise Exception("Error: you didnt complete the string. FINISH IT.")
    
print(codepy) # using exec for testing purposes 
