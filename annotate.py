#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Command line annotation tool.

This script prints each word of a text file to the command line
and takes the user's input as annotation.

Annotation is saved to pickle file and can be continued at last
annotated sentence.

@Author: Hanna Winter
"""

import sys, argparse
import pickle
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize



parser = argparse.ArgumentParser()
#mandatory argument: text feil to be annotated
parser.add_argument("file", help="Name a text file.", type=str)
#optional argument: index of sentence that was annotated last
parser.add_argument("-i", "--index", help="Indicate index where you left off.", type=str, default="0")
args = parser.parse_args()

file = args.file

#open file containing text to be annotated
with open(file, "r") as f:
	text = f.read()

index = int(args.index)

#og filename is taken for new file containing annotations
file_name = file[:-4] + "-ANNO.pickle"

#load annotations and continue at last annotated sentence
if index != 0:
	try:
		annotation = pickle.load(open(file_name, "rb"))
	except OSError:
		annotation = []
else:
	try:
		#check if previous annotation exists to prevent overwriting
		annotation = pickle.load(open(file_name, "rb"))
		print("There exists an annotation for your file. Do you want to load it? [y/n]")
		answer = input()
		#answer must be either of: (y, n, yes, no)
		valid_answer = False
		while not valid_answer:
			if answer == "y" or answer == "yes":
				valid_answer = True
				#annotation = pickle.load(open(file_name, "rb"))
				#load last index to continue annotation
				#check if there is an index from the last annotation
				print("check")
				with open("index.txt", "r") as f:
					index = int(f.read())
				print("You left off at sentence %s. Continue here? [y/n]" %str(index))
				ans = input()
				valid_ans = False
				while not valid_ans:
					if ans == "y" or ans == "yes":
						valid_ans = True
					elif ans == "n" or ans == "no":
						valid_ans = True
						print("At what index do you want to continue?")
						index = input()
						while not index.isdigit():
							print("Index must be integer. Please type your last index.")
							index = input()
						index = int(index)
					else:
						print("Please answer with [y/n] or [yes/no].")
						ans = input()
			elif answer == "n" or answer == "no":
				valid_answer = True
				print("Starting annotation from first sentence.")
				annotation = []
			else:
				print("Please answer with [y/n] or [yes/no].")
				answer = input()
	except OSError:
		annotation = []



#get list of sentences
sentences = sent_tokenize(text)
#TODO: define your labels (to avoid empty labels delete "" from tuple)	
labels = ("",)

#iterate over sentences and their words and take input as label
for s in sentences[index:]:
	i = sentences.index(s)
	print("Press enter to continue or write 'exit' to stop annotation.")
	user = input()
	if user == "exit":
		break
	print(s)
	words = word_tokenize(s)
	for w in words:
		print(w)
		label = input()
		if label == "exit":
			#index of sentence which was annotated last
			print("Please finish annotating the current sentence before exiting.")
		else:
			#only accepts pre-defined labels , or "exit"
			while label not in labels:
				print("Label not valid. Options: %s" %str(labels))
				label = input()
			annotation.append((w, label))
	i_w = 0
	if label == "exit":
		break


#save new annotation to pickle file
with open (file_name, "wb") as fp:
	pickle.dump(annotation, fp)

#save index to file
with open("index.txt", "w") as f:
	f.write(str(i))

print(annotation)
print("Your annotation was saved to: %s ." %file_name)
print("The index of your last annotated sentence was saved to: index.txt .")