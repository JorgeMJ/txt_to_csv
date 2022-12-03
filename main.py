#!/usr/bin/env python

'''
PURPOSE
	Transform TXT files into CSV.

INPUT/OUTPUT FILES
	This program takes TXT files containing list of scientific publications and outputs a CSV file per input file
with the same filename. Additionally, it creates a file called '_all_publications.csv' that holds all the
publications transformed into CSV. The input TXT files are expected to reside in a folder called 'citation_project'
located in the same file as this present file is.
	All output files will be stored in a newly created folder called 'csv_files'.

INPUT FILE FORMAT
	The input .TXT are expected to have each field delimited by a newline and the different entries (i.e. publications)
are expected to be separated by two newlines.

DELIMITER VALUE
	The default CSV files delimiter character is the comma (,). The delimiter used in this program to separate values is
the dollar symbol ($) specified under the constant 'DELIMITER'. The reason for choosing $ as the separating value is due
to the fact that some of the values of the input TXT files contain commas (,). 

	Also, the semicolon (;) is considered by Excel as a marker for a new cell, for this reason the ';' of the input
TXT is replaced by ampresand (&).

'''

import glob
import os
import csv

DELIMITER = '$'

def main():

	all_publications = []
	path = '.\\citation_project\\*'
	files = glob.glob(path) 

	if not os.path.exists('csv_files'):
		os.mkdir('csv_files')

	for filename in files:		
		base_filename = os.path.basename(filename).split('.')[0]
		publications = []
		clean_publications = []
		
		with open(filename, 'r',encoding='utf-8-sig') as in_file:
			read = in_file.readlines()
			current_publication = []

			for line in read:
				if line != '\n':
					current_publication.append(line.strip().strip(',').replace(';', '&'))
				else:
					#This prevents from adding an empty array to 'publications' due to the possible
					# presence of more than 2 consecutive newlines
					if current_publication != []:
						publications.append(current_publication)
					current_publication = []
			#This line adds the last 'current_publication' to 'publications' list		
			publications.append(current_publication)

			for pub in publications:
				if len(pub) >= 10 :
					fixed_fields = pub[:9]
					variable_fields = "_".join(pub[9:-1])
					keywords = pub[-1].replace('& ', ', ')
				else:
					fixed_fields = pub
					variable_fields = None
					keywords = None

				clean_publications.append(fixed_fields + [variable_fields] + [keywords])
			
			all_publications += clean_publications

			with open('csv_files/'+base_filename+".csv", "w", newline="", encoding='utf-8-sig') as out_file:
				writer = csv.writer(out_file, delimiter=DELIMITER)
				writer.writerow(['Authors', 'Title', 'Journal', 'Volumen', 'Year', 'num', 'ISSN', 'link1', 'link2', 'Abstract', 'Keywords'])
				writer.writerows(clean_publications)

	#This file contains all publications
	with open('csv_files/_all_publications.csv', "w", newline="", encoding='utf-8-sig') as out_file:
				writer = csv.writer(out_file, delimiter=DELIMITER)
				writer.writerow(['Authors', 'Title', 'Journal', 'Volumen', 'Year', 'num', 'ISSN', 'link1', 'link2', 'Abstract', 'Keywords'])
				writer.writerows(all_publications)

if __name__ == "__main__":
	main()