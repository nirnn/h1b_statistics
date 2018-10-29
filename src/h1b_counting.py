import sys
import constants as ct

# return the column number in the header, given a string to search
def locate_idx(str, lst, is_first = True):
	idx = [i for i, elem in enumerate(lst) if str in elem]
	if len(idx) == 0: sys.exit("Cannot locate %s in header. Program aborts!" % str)
	idx = idx[0] if is_first else idx[-1]
	return idx

# write a sorted output file, given a dictionary
def write_top_items_sorted(filename, header, dict, counter, n = 10):
	dict_sorted = [x[0] for x in sorted(dict.items(), key = lambda x : (-x[1], x[0]))]
	with open(filename, "w") as opf:
		opf.write(header + "\n")
		for e in dict_sorted[:n]:
			opf.write(f"{e};{dict[e]};{dict[e]/counter*100:.1f}%\n")

def main():
	# check input params
	if len(sys.argv) < 4: sys.exit(f"usage: {sys.argv[0]} <input file name> <occupations output file name> <states output file name>")
	input_filename = sys.argv[1]
	occupations_filename = sys.argv[2]
	states_filename = sys.argv[3]

	# read header
	file = open(input_filename, encoding="utf8", mode="r")
	header = file.readline().split(";")
	status_idx = locate_idx("STATUS", header)
	soc_idx = locate_idx("SOC_NAME", header)
	state_idx = locate_idx("_STATE", header, False)

	# read input file to data sets
	lines = file.read().split("\n")
	occupations = {}
	states = {}
	counter = 0
	for line in lines:
		line = line.split(";")
		if len(line) < state_idx: continue
		if(line[status_idx] == "CERTIFIED"):
			occupations[line[soc_idx]] = (occupations[line[soc_idx]] + 1) if line[soc_idx] in occupations else 1
			states[line[state_idx]] = (states[line[state_idx]] + 1) if line[state_idx] in states else 1 
			counter += 1

	# output
	write_top_items_sorted(occupations_filename, ct.OCCUPATIONS_HEADER, occupations, counter)
	write_top_items_sorted(states_filename, ct.STATES_HEADER, states, counter)

if __name__ == "__main__":
	main()