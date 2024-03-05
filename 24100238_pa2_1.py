# -*- coding: utf-8 -*-
"""RollNumber_PA2_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N8v6WLilsXiSS6hktvu7yAxn6znEbZsU

# PA2.1 - Building your first Chatbot: Aleeza

### Introduction

In this notebook, you will be implementing your own version of the first ever Chatbot, ELIZA.

### Instructions

- Follow along with the notebook, filling out the necessary code where instructed.

- <span style="color: red;">Read the Submission Instructions and Plagiarism Policy in the attached PDF.</span>

- <span style="color: red;">Make sure to run all cells for credit.</span>

- <span style="color: red;">Do not remove any pre-written code.</span> We will be using the `print` statements to grade your assignment.

- <span style="color: red;">You must attempt all parts.</span> Do not assume that because something is for 0 marks, you can leave it - it will definitely be used in later parts.

## Background: ELIZA
#### The first ever Chatbot.

<div style="display: flex; justify-content: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/7/79/ELIZA_conversation.png" width="400" height="250" alt="ELIZA Conversation">
</div>

This Chatbot was released in 1966 (before the term Chatbot even existed) by Joseph Weizenbaum of MIT. This was a revolutionary program that allowed humans to converse with a computer. As you may have predicted, this was a retrieval-based system, very different from the "language models" of today. However, you may be surprised by how well it performed despite the simplicity of the system. Here is part of a conversation someone had with ELIZA, from the original paper (the capitalised sentences are ELIZA's responses):
\
\
Men are all alike.\
IN WHAT WAY\
They're always bugging us about something or other.\
CAN YOU THINK OF A SPECIFIC EXAMPLE\
Well, my boyfriend made me come here.\
YOUR BOYFRIEND MADE YOU COME HERE\
He says i'm depressed much of the time.\
I AM SORRY TO HEAR YOU ARE DEPRESSED\
It's true. I am unhappy.\
DO YOU THINK COMING HERE WILL HELP YOU NOT TO BE UNHAPPY\
......

The program used certain programmed rules to "transform" the input into the output. In order to do this, the program must first decompose the sentence based on certain criteria and then reassemble it based on the predefined assembly specifications. For example, if it is provided with the input sentence, "It seems that you hate me", it may be decomposed into:

1) It seems that
2) you
3) hate
4) me

Of these, (2) and (4) are recognised as key words. The program can then use the remaining sections of the sentence based on pre-defined rules to construct an output. For example, it may be programmed with the rule:

decomposition template:\
(0 YOU 0 ME)\
and the reassembly rule:\
(WHAT MAKES YOU THINK I 3 YOU).

Here, the "0" represents any number of words, whereas the "3" represents the 3rd part of the sentence from before. Hopefully, this makes the implementation a little clearer. If not, don't worry as you'll understand how it works once you start implementing your own version!

For more details on the original ELIZA implementation, [Click Here](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf).

## Specifications

As described above, your task will be to first read in a user string, then modify it to provide an output (sometimes subtly, sometimes drastically, depending on the input string). This should be easy to do with the regex library, the specifics of which were discussed in class.

\
Your program should be able to handle all 1st and 2nd person pronouns, all 1st and 2nd person subject-verb pairs with the verb be and all possible forms of the verb. If it is unclear what is meant by this, you might want to do some googling.

\
An example is as follows:

Regular Expression: I am (.*)\
Response: How long have you been %1?

Example Input that matches: I am sad.\
Example Response: How long have you been sad?

Please note that this is a simplified version of the chatbot, and the original bot had a much more complex algorithm behind it.

You will have two tables to store all the logic of your bot:
1. Reflection Table
2. Response Table

These will be described in detail in the cells below.

## Imports

These are the ONLY imports you can use for this part of the assignment.
"""

import json
import re
import random

from google.colab import drive
drive.mount('/content/drive')

"""## Tables

These are your reflection and response tables.

#### Reflection Table

This table serves to convert your pronouns from first person to second person and vice versa. You should list all forms of the pronouns and their corresponding "reflection". (eg. i : you)\
\
You should also do the same for all the forms of the verb "be". (eg. am : are)\
\
Note: You do not need to add plural pronouns such as "we".\
\
This table will be represented as a dictionary. (The first entry is listed as an example below)
"""

reflectionTable = {
    "i": "you",
    "am": "are",
    "my": "your",
    "mine": "yours",
    "me": "you",
    "myself": "yourself",
    "are": "am",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "yourself": "myself"
}

reflectionTable2 = {
    "i": "you",
    "am": "are",
    "my": "your",
    "mine": "yours",
    "me": "you",
    "myself": "yourself",
    "are": "am",
    "your": "my",
    "yours": "mine",
    "you": "I",
    "yourself": "myself"
}

"""#### Response Table

This table is in the form of a nested list. Each entry is a list, with the first term being your regular expression and the second term being a list of possible responses. "%n" represents the nth match. You will need to handle this in your code later when replacing the relevant parts of the text.

Since this is a fairly large table, you will fill out the regular expressions and the responses in a json file: "responseTable.json"

\
In this table, you must include ALL subject-verb pairs for the verb "be". Do this for first, second and third person pronouns. (eg. I am ...) You must add at least 3 appropriate responses for each of these pairs. You need not account for the contracted versions of the pairs. But, DO include the corresponding question statements for each of these pairs. You can assume there will be no past-tense or future-tense inputs.\
\
Furthermore, in the case that you encounter no matches, you must have fallbacks. Due to this, you must also account for the following cases:
1. (I feel ...), (I want ...), (I think ...)
2. Subject with an unknown verb
3. An unrecognised question
4. Any string

Include 4 or more responses for these cases as they will likely be encountered more often.\
\
Lastly, add at least 3 more subject-verb pairs, with at least 1 response each. These can be anything you like. Have fun with it (but keep it appropriate).\
\
For example:

Regex: I voted for (.*)

Response: How did voting for (.*) make you feel?

Please ensure the correct order, as you will only be checking the first match later on.\
Once again, an example entry has been provided.
"""

# Add entries in the JSON file

responseTable = json.load(open(fr'/content/drive/MyDrive/GEN-AI/PA2/responseTable.json'))

"""## Helper Functions (Optional)

If you wish to modularise your code to make your life simpler in the upcoming cells. Please define your helper functions here.
"""

# Code here
def ends_with_special_character(s):
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '\\', '|']
    return s.endswith(tuple(special_characters))

"""## Aleeza Class

This is the class you will be implementing all of your bot's functionality in. As you will see, this is very straightforward and most of the actual work will be done while writing the response table. We will call our version Aleeza.
"""

class Aleeza:
  def __init__(self, reflectionTable, responseTable):
    """
    Initiliase your bot by storing both the tables as instance variables.
    You can store them any way you want. (Dictionary, List, etc.)
    """
    self.reflectionTable = reflectionTable
    self.reflectionTable2 = reflectionTable2
    self.responseTable = responseTable

  def reflect(self, text):
    """
    Take a string and "reflect" based on the reflectionTable.

    Return the modified string.
    """
    words = text.lower().split()
    reflected_words = []
    for i, word in enumerate(words):
        if word in self.reflectionTable and i==len(words)-1:
            reflected_words.append(self.reflectionTable[word])
        elif word in self.reflectionTable and (words[i+1] == "are" or words[i+1] == "were"):
            reflected_words.append(self.reflectionTable2[word])
        elif word in self.reflectionTable:
            reflected_words.append(self.reflectionTable[word])
        else:
            reflected_words.append(word)
    return ' '.join(reflected_words)

  def respond(self, text):
    """
      Take a string, find a match, and return a randomly
      chosen response from the corresponding list.

      Do not forget to "reflect" appropriate parts of the string.

      If there is no match, return None.
    """
    for pattern, responses in self.responseTable:
        match = re.match(pattern, text.lower())
        if match:
            itr = 1
            response = random.choice(responses)
            while(itr != len(match.groups())+1):
                match_group = match.group(itr)
                if ends_with_special_character(match_group):  # Excluding fullstop/question mark kinda stuff from the end of the string
                    match_group = match_group[:-1]
                response = response.replace(f'%{itr}', self.reflect(match_group))
                itr+=1
            return response
    return None

therapist = Aleeza(reflectionTable, responseTable)
s = "Hi, how are you?"
print(therapist.respond(s))

"""## Test your Bot

You can use this interface to manually check your bot's responses.
"""

def command_interface():
    print('Aleeza\n---------')
    print('Talk to the program by typing in plain English.')
    print('='*72)
    print('Hello.  How are you feeling today?')

    s = ''
    therapist = Aleeza(reflectionTable, responseTable)
    while s != 'quit':
        try:
            s = input('> ')
        except EOFError:
            s = 'quit'
        print(s)
        while s[-1] in '!.':
            s = s[:-1]
        print(therapist.respond(s))

command_interface()

"""## Test Sentences

After testing your bot, you have likely seen that it does not work very well yet. This goes to show the immense amount of work that was put into the original ELIZA program.\
In any case, having concocted all of your (hopefully) appropriate responses, you now need to demonstrate your bot handling all the cases listed above. To do this, you must provide an example sentence handling each of the regular expressions you have listed in your response table.
"""

test_sentences = [
    "Hi",
    "I hope you are doing well.",
    "I am not enjoying this anymore.",
    "She cheated on me.",
    "I feel betrayed.",
    "I believe she deserved better.",
    "Because everytime I used to ask her out, she made an excuse.",
    "I want you to listen to me.",
    "You are my friend.",
    "vicnroirngv.",
    "What would I do without you?",
    "I would die if you were not there for me.",
    "Because I would have been in so much depression if you were not there.",
    "Dude, do not say that.",
    "I understand you are just a bot."

]

def get_responses(sentence_list, bot):
    """
    Get a response for each sentence from the list and return as a list.
    """

    # Code here
    responses = list()
    therapist = Aleeza(reflectionTable, responseTable)
    for i in test_sentences:
        responses.append(therapist.respond(i))
    return responses

therapist = Aleeza(reflectionTable, responseTable)

for pair in zip(test_sentences, get_responses(test_sentences, therapist)):
    print('='*72)
    print(pair[0])
    print(pair[1])

"""# Giving Aleeza Emotional Intelligence

In the next part of the assignment, you will be giving your chatbot some emotional intelligence. This will be done by training a simple emotion classification model. You will then use this model to classify the sentiment of the user's input and respond accordingly.\
\
How our logic will work is as follows:
1. If there is a match in the response table, we will use the response from the table.
2. If there is no match, we will classify the emotion of the input and respond accordingly.

The model we will use is a simple Naive Bayes Classifier. This is a simple model that works well with text data. You will be using the `scikit-learn` library to train the model, and the huggingface `datasets` library to get the data.

## Imports

These are the ONLY imports you can use for this part of the assignment.
"""

!pip install --upgrade pyarrow
!pip install datasets

import datasets
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

"""## Dataset

We will be using the `emotion` dataset from the `datasets` library. This dataset contains text data and the corresponding emotion. You will use this data to train your model. Load this dataset using the `load_dataset` function from the `datasets` library.

Next, split the dataset into training and testings sets.\
(HINT: This has already been done for you in the dataset you loaded)
"""

"""
Load the emotion dataset from Hugging Face
"""

dataset = datasets.load_dataset("emotion") # Code here

dataset

"""
Split the dataset into training and testing sets
"""

# Code below
train_data = dataset["train"]["text"]
train_labels = dataset["train"]["label"]
test_data = dataset["test"]["text"]
test_labels = dataset["test"]["label"]

"""## Training the Model

Just like in your previous assignment, you will now train the model and evaluate it.
"""

"""
Vectorise the data and train the model
"""

# Code here
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(train_data, train_labels)

"""
Predict on the test set
"""
predicted_labels = model.predict(test_data) # Code here


"""
Print classification report
"""
print(classification_report(test_labels, predicted_labels))

"""## Putting it all together

Now that we have our classification model, we can modify our chatbot to use it.

First, we will remove the fallback responses from our response table, i.e. the following cases:
1. (I feel ...), (I want ...), (I think ...)
2. Subject with an unknown verb
3. An unrecognised question
4. Any string

Remove these and save your response table as "responseTable2.json".
"""

# Make a new file "responseTable2.json" and add your modified table to it

responseTable = json.load(open(fr'/content/drive/MyDrive/GEN-AI/PA2/responseTable2.json'))

"""#### Emotion Response Table

This table will be a dictionary with the emotions as keys and a list of possible responses as values. You should include at least 2 responses for each emotion.
"""

# Add responses below

emotionTable = {
    0: [  # sadness
        "Oh no, the world is ending! (Just kidding, it's not.) What's got you feeling blue?",
        "Holly Molly, I'm sorry to hear that. Do you want to talk more about it? (not a gossip monger but generally curious to listen to your story)",
        "It's okay to feel sad sometimes (even I feel sad). Is there anything specific that's bothering you? SPILL!",
        "Feeling sad is like getting a bad haircut. It sucks, but it'll grow back. What's the story?"
    ],
    1: [  # joy
        "YAAHOOO! That's great to hear! What's making you feel this way?",
        "Woo-hoo! Sounds like someone's got a case of the happies! Let's talk about it a bit more.",
        "I'm glad you're feeling this way! Anything else exciting happening in your life?"
    ],
    2: [  # love
        "Love is a wonderful feeling. What's making you feel loved?",
        "Aww, love is in the air! Or maybe that's just a passing pigeon. What's got you feeling all warm and fuzzy?",
        "It's beautiful to feel loved but sometimes, it hurts. I love you too but tell me about your story?"
    ],
    3: [  # anger
        "I understand that anger can be overwhelming. What's causing your anger?",
        "oh, someone's got their grumpy pants on! What's got you seeing red?",
        "Why are angry? STOP SCREAMING AND COME TO YOUR SENSES FOR GOD's SAKE. Is there something in particular that's making you angry?",
        "OMG, Daddy chill!"
    ],
    4: [  # fear
        "BHOOOOOO, you scared? lil boi issok to feel this way. Temme more about it."
        "It's okay to feel afraid. Can you tell me what you're afraid of?",
        "Fear is a common emotion. I am afraid of brocolli. Is there something specific that's making you feel afraid?"
    ],
    5: [  # surprise
        "AHHHHHHHHH. Surprises can be exciting! What surprised you?",
        "I love surprises! (gimme surprise marks). What was the surprising moment in your life?"
        "A surprise is just life's way of saying, 'Hey, pay attention!' What's the plot twist in your day?"
    ]
}

"""### Modifying your Chatbot

You will now modify your chatbot to use the emotion classifier. If there is a match in the response table, we will use the response from the table. If there is no match, we will classify the emotion of the input and respond accordingly.
"""

class IntelligentAleeza(Aleeza):
    def __init__(self, reflectionTable, responseTable, emotionTable, classifier):
        """
        Initialise your bot by calling the parent class's __init__ method,
        and then storing the emotionTable as an instance variable.

        Next, store the classification model as an instance variable.
        """

        # Code here
        super().__init__(reflectionTable, responseTable)
        self.emotionTable = emotionTable
        self.classifier = classifier

    def smart_respond(self, text):
        """
        Take a string, call the parent class's respond method.
        If the response is None, then respond based on the emotion.
        """

        # Code here
        response = super().respond(text)
        if response is None:
            emotion = self.classifier.predict([text])
            print("emotion",emotion)
            responses = self.emotionTable.get(emotion[0], [])
            response = random.choice(responses) if responses else "I'm not sure how to respond to that."
        return response

"""## Test your New Bot

Randomly select 5 sentences from the test set and test your bot. You should see that it now responds with an appropriate message based on the emotion detected in the input (when there is no match).
"""

def get_responses(sentence_list, bot):
    """
    Get a response for each sentence from the list and return as a list.
    Use your new smart_respond method.
    """

    # Code here
    responses = []
    for sentence in sentence_list:
        response = bot.smart_respond(sentence)
        responses.append(response)
    return responses

"""
Create an instance of the IntelligentAleeza class
"""
intelligent_therapist = IntelligentAleeza(reflectionTable, responseTable, emotionTable, model) # Code here

"""
Get 5 random test instances from the test data
"""

# Code here
print("test_data",test_data)
test_instances = random.sample(test_data, 5)


"""
Get responses from the intelligent_therapist
"""

responses = get_responses(test_instances, intelligent_therapist)


"""
Print the test instances and the responses
"""
for pair in zip(test_instances, responses):
    print('='*72)
    print(pair[0])
    print(pair[1])

"""# Fin."""