# Annotation Tool
command line tool for annotating tokens for Python 3

## Prerequisites
You need to provide a .txt-file containing the text you want to annotate.

The script uses nltk for sentence and word tokenization. Installation:
```bash
$ pip3 install nltk
```
 The nltk sentence tokenizer highly depends on punctuation, so make sure your text file contains complete sentences. If this is not the case, nltk might interpret one sentence as multiple which affects the annotation. The tool would print you multiple sentences as one long sentence, and exiting would reset the annotation of this "sentence".

## Description
The annotation tool works via the command line. It prints each sentence of your text file and lets you annotate word by word. To do so, it shows you word after word and takes your input as label. 

If you exit the tool, your progress so far is saved and you can continue with the last unannotated sentence next time you run the script. You can exit the tool any time but exiting during the annotaion of a senetence will reset the annotation of this one sentence.

### Pre-defined Labelset
Before you start, you need to pre-define the labels you want to use for your annotations. You can do so in line 94:
```python
labels = ("",)
```

### Commandline Interface
To avoid labels which were not defined, the tool compares the user input with the set of labels. 

The annotation is saved to a pickle file and can be continued at the last annotated sentence the next time you run the script. It checks if an annotation file for your text file exists and asks you, if you want to continue where you left off or start from scratch. The annotation can only be paused between sentences. 

To start off at your last sentence, you can indicate its index as command line argument:

```bash
usage: annotate.py [-h] [-i INDEX] file

positional arguments:
  file                  Name a text file.

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        Indicate index where you left off.
```

### Running the Tool
Run the tool via the Linux command line. You can test it using the example text from 'The Little Prince' (don't forget to define your labels first):
```bash
$ python3 annotate.py example-text.txt
```

#### Interactive Options
There are a few commands you can issue while using the tool:
* *exit*: exits tool; annotation is saved until last sentence that was completely annotated
* *annotation*: prints the word-label pairs that were annotated so far
* *sentence*: prints the sentence you are currently annotating

# Author
* Hanna Winter