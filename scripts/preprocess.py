import sys
import os

infile = sys.argv[1]
f_out = open(infile+".out", "w")

with open(infile) as f_in:
    for line in f_in:
    	filtered_line = ""
        for char in line:
        	if char in [' ', '.'] or char.isalpha():
        		filtered_line += char.lower()
        f_out.write(filtered_line)

os.remove(infile)
os.rename(infile+".out", infile)