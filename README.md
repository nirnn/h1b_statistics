# H1B Statistics
This is a simple and straight forward implementation to the h1b statistics challenge.
The challenge is implemented in native python, without any added modules frameworks or libraries.
We read the input file header, and located the desire columns.
We than read the input file, line by line, counting for the relevant data, using a dictionary as a counter. 
Note that I decided not to use any high performance data structures (such as counter collection) since code runs quite fast on the given input files.