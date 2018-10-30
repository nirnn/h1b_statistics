import time
import sys
import re 

# data structure to hold needed counts
class Data:
	def __init__(self):
		self.occupations = {}      # dictionary to count occupations occurrences
		self.states      = {}      # dictionary to count states occurrences
		self.counter     = 0       # counts the number of total occurrences
	def add(self, occupation, state):
		self.occupations[occupation] = (self.occupations[occupation] + 1) if occupation in self.occupations else 1
		self.states[state] = (self.states[state] + 1) if state in self.states else 1 
		self.counter += 1

# class to hold data and perform main read / write operations
class FileData:
	def __init__(self, filename):
		# return string index in a list; if multiple occurrences, return either first or last
		def locate_idx(lst, str , first):
			idx = [i for i, elem in enumerate(lst) if str in elem]
			if len(idx) == 0: 
				sys.exit("Cannot locate %s in header. Program aborts!" % str)
			return(idx[0] if first else idx[-1])

		self.data = Data()
		# read input file to data sets - read header and extract needed indexes
		with open(filename, encoding="utf8", mode="r") as file:
			header = file.readline().split(";")
			needed_cols = len(header)
			status_idx = locate_idx(header, "STATUS", True)
			soc_idx = locate_idx(header, "SOC_NAME", True)
			state_idx = locate_idx(header, "_STATE", False)
			lines = file.read().split("\n")
			for line in lines[:-1]:                    # go over all lines, but last one (which is empty)
				# split line by the separator ; but ignore cases where it's within quotes
				if line.count(";") + 1 != needed_cols: # too many ; => line has quotes  
					line = re.sub(r'".*?"'," ", line)  # Replace quoted text with empty strings
				line = line.split(";")                 # Now split the line safely
				if line[status_idx] == "CERTIFIED":    # Count only CERTIFIED cases
					self.data.add(line[soc_idx], line[state_idx])

	def write(self, occupations_filename, states_filename):
		# constants
		OCCUPATIONS_HEADER = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
		STATES_HEADER      = "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
		# write a sorted output file, given a dictionary
		def write_sorted(dict, filename, header):
			dict_sorted = [x[0] for x in sorted(dict.items(), key = lambda x : (-x[1], x[0]))]
			with open(filename, "w") as opf:
				opf.write(header + "\n")
				for e in dict_sorted[:10]:
					opf.write("%s;%s;%.1f%%\n" %(e,dict[e],dict[e]/self.data.counter*100))
		write_sorted(self.data.occupations, occupations_filename, OCCUPATIONS_HEADER)
		write_sorted(self.data.states, states_filename, STATES_HEADER)

def main():
	if len(sys.argv) < 4: 
		sys.exit("usage: %s <input file name> <occupations output file name> <states output file name>" % sys.argv[0])
	input_filename = sys.argv[1]
	occupations_filename = sys.argv[2]
	states_filename = sys.argv[3]
	
	filedata = FileData(input_filename)
	filedata.write(occupations_filename, states_filename)

if __name__ == "__main__":
	#start = time.time()
	main()
	#end = time.time()
	#print(end - start)