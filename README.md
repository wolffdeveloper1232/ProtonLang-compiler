proglang is a transpiled language that is turing complete.
commands:
out() -> print()
same a b { ... } -> if a==b:
loop { ... } -> while True:
stop: -> break

other:
to set var
var: myvar = "value" ;

or for input:
var: user = in: ;

what ever is in () does not get edited, and because it transpiles to python, you can do stuff like:
out("whats your name?")
var: user = in: ;
out("Hello " + user + "!")

to increase or decrease i var thats a number do:
inc: counter;
to increase or do:
dec: counter;
to decrease.

there is a already made example program that you can transpile into python.

replace the code var with your in code inside of the code for the compiler. then use python3 to run it. then copy and paste the output into a different .py file, and run that file. thats how you make your own code.
