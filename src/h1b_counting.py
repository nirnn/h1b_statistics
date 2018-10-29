import sys
import constants as ct
import re 

# return the column number in the header, given a string to search
def locate_idx(str, lst, is_first = True):
	idx = [i for i, elem in enumerate(lst) if str in elem]
	if len(idx) == 0: 
		sys.exit("Cannot locate %s in header. Program aborts!" % str)
	idx = idx[0] if is_first else idx[-1]
	return idx

# write a sorted output file, given a dictionary
def write_top_items_sorted(filename, header, dict, counter, n = 10):
	dict_sorted = [x[0] for x in sorted(dict.items(), key = lambda x : (-x[1], x[0]))]
	with open(filename, "w") as opf:
		opf.write(header + "\n")
		for e in dict_sorted[:n]:
			opf.write("%s;%s;%.1f%%\n" %(e,dict[e],dict[e]/counter*100))

def main():
	# check command line parameters
	if len(sys.argv) < 4: 
		sys.exit("usage: %s <input file name> <occupations output file name> <states output file name>" % sys.argv[0])
	input_filename = sys.argv[1]
	occupations_filename = sys.argv[2]
	states_filename = sys.argv[3]

	# read header and extract needed indexes
	file = open(input_filename, encoding="utf8", mode="r")
	header = file.readline().split(";")
	needed_cols = len(header)
	status_idx = locate_idx("STATUS", header)
	soc_idx = locate_idx("SOC_NAME", header)
	state_idx = locate_idx("_STATE", header, False)
	
	# read input file to data sets
	lines = file.read().split("\n")
	occupations = {}      # dictionary to count occupations occurrences
	states = {}           # dictionary to count states occurrences
	counter = 0           # counts the number of total occurrences
	for line in lines:
		# split line by the separator ; but ignore cases where it's within quotes
		if line.count(";") != needed_cols - 1: # too many ; => line has quotes  
			line = re.sub(r'".*?"'," ", line)  # Replace quoted text with empty strings
		line = line.split(";")                 # Now split the line safely
		if len(line) != needed_cols:
			continue
		if(line[status_idx] == "CERTIFIED"):   # Count only CERTIFIED cases
			occupations[line[soc_idx]] = (occupations[line[soc_idx]] + 1) if line[soc_idx] in occupations else 1
			states[line[state_idx]] = (states[line[state_idx]] + 1) if line[state_idx] in states else 1 
			counter += 1
			
	# write output to files
	write_top_items_sorted(occupations_filename, ct.OCCUPATIONS_HEADER, occupations, counter)
	write_top_items_sorted(states_filename, ct.STATES_HEADER, states, counter)

if __name__ == "__main__":
	main()