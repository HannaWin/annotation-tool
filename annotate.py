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



def save_anno_to_txt(anno):
	"""saves completed annotation to txt file"""
	f_name = file[:-4] + "-ANNO.txt"
	with open(f_name, "w") as ft:
		for sent in anno:
			ft.write('\n'.join('%s %s' % tup for tup in sent))
	print("Your annotation was saved to: %s" %f_name)



def save_anno_to_excel(anno):
	"""saves completed annotation to excel file"""
	import openpyxl
	xlsx = openpyxl.Workbook()
	sheet = xlsx.active
	for sent in anno:
		for row in sent:
			sheet.append(row)
	f_name = file[:-4] + "-ANNO.xlsx"
	xlsx.save(f_name)
	print("Your annotation was saved to: %s" %f_name)



def save_as_conll(annotation):
	"""saves annotation in conll format;
	input must be list of list of tuples"""
	conll = []
	for sentence in annotation:
		j = annotation.index(sentence)
		for anno in sentence:
			i = sentence.index(anno)
			tup = (str(j+1) + "-" + str(i+1), anno[0], "_", "_", anno[1])
			conll.append(tup)
	f_name = file[:-4] + "-ANNO.conll"
	with open(f_name, "wt") as f:
		for tup in conll:
			for l in tup:
				f.write(l + "\t")
			f.write("\n")
	print("Your annotation was saved to: %s" %f_name)



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
	anno_sent = []
	for w in words:
		print(w)
		label = input()
		i_w = words.index(w)
		while label not in labels:
			if label == "sentence":
				print(s)
				print(w)
				label = input()
			elif label == "annotation":
				print(annotation)
				print(w)
				label = input()
			elif label == "exit":
				break
			else:
			#only accepts pre-defined labels , or "exit"
				print("Label not valid. Options: %s" %str(labels))
				print(w)
				label = input()
		if label == "exit":
			print("Exiting annotation.")
			index = i
			break
		elif label in labels:
			anno_sent.append((w, label))
	if len(anno_sent) == len(words):
		annotation.append(anno_sent)
	i_w = 0
	if label == "exit":
		break
	elif label == "sentence":
		print(s)
	if len(sentences) == sentences.index(s)+1:
		print("Annotation complete!")
		#save_anno_to_txt(annotation)
		save_anno_to_excel(annotation)
		save_as_conll(annotation)




#save new annotation to pickle file
with open (file_name, "wb") as fp:
	pickle.dump(annotation, fp)

#save index to file
with open("index.txt", "w") as f:
	f.write(str(index))

print("Your annotation was saved to: %s ." %file_name)
print("The index of your last annotated sentence was saved: %s ." %index)



#print(annotation)

