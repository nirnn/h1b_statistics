# H1B Statistics
This is a simple and straight forward implementation to the h1b statistics challenge.
I implemented the challenge is in native python, without any added modules frameworks or libraries.

# Implementation
1. Read the input file header, and locate all the desired columns.
2. Read the input file, line by line, counting for the relevant data, using a dictionary as a counter.
3. Output the needed output, according to the given format.

# Notes
1. I'm using a dictionary to count data. This works well empirically on the given examples.
I can easily explain this for the states data, since there are only 50 states.
The number of occupations is larger, but not too large (e.g. there are less than 1000 occupations for the largest data set).
Some other simple alternative could have been using python collections, in particular counter, but there was no need to.
2. I read the entire file into memory. Again, I could have used some kind of serialization, 
going iteratively line by line. Since my approach worked well empirically, even on large input files,
I didn't find any need to do something more sophisticated. 
3. I filter for CERTIFIED status. I ignore all other status, including CERTIFIED-WITHDRAWN.