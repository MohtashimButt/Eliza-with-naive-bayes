import json
import re
import random

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

responseTable = json.load(open(fr'responseTable.json'))
def ends_with_special_character(s):
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '\\', '|']
    return s.endswith(tuple(special_characters))

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

# intelligent_therapist = IntelligentAleeza(reflectionTable, responseTable, emotionTable, model) # Code here

# """
# Get 5 random test instances from the test data
# """


# """
# Get responses from the intelligent_therapist
# """

# # responses = get_responses(test_instances, intelligent_therapist)


# """
# Print the test instances and the responses
# """
# # for pair in zip(test_instances, responses):
# #     print('='*72)
# #     print(pair[0])
# #     print(pair[1])

# """# Fin."""