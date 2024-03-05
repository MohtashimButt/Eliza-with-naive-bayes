# Eliza-with-naive-bayes

## Early Eliza
ELIZA is an early natural language processing computer program developed from 1964 to 1967[1] at MIT by Joseph Weizenbaum.[2][3] Created to explore communication between humans and machines, ELIZA simulated conversation by using a pattern matching and substitution methodology that gave users an illusion of understanding on the part of the program, but had no representation that could be considered really understanding what was being said by either party.

## What's new in my version of Eliza?
I use RegEx for deciphering the input prompts, added a naive bayes classifier to analyze the sentiments of the prompt, and trained the model in a way that it responds according to the sentiment of the input prompt. In short, I gave emotional intelligence to Eliza using Naïve Bayes Classifier.

## File Descriptions
- `24100238_PA2_1.ipynb`: The notebook contian the code for the raw Eliza chatbot and its training on Naïve Bayes Classifier.
- `24100238_PA2_1.py`: This is just a `.py` version of `24100238_PA2_1.ipynb`.
- `responseTable.json`: This file contains the format of Eliza's responses.
- `responseTable2.json`: This file contains the format of Intelligent Eliza's responses.

## How to use it?
- Clone the repo first using `git clone https://github.com/MohtashimButt/Eliza-with-naive-bayes`
- Go to `24100238_PA2_1.ipynb` and run every cell.

# Reference
Weizenbaum, J. (1966). ELIZA—a computer program for the study of natural language communication between man and machine. Communications of the ACM, 9(1), 36-45.
