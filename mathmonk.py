import nltk
import numpy as np
from corpus import read_corpus
from util import MathProcessor
from adapters import MathAdapter, ChatterAdapter
from nltk import word_tokenize, sent_tokenize

class MathMonk():
    """The MathMonk is a Bot which takes a input in Natural Language, 
    performs calculation and then returns the output in Natural Language.
    
    The MathMonk performs two important steps:
    1. Classifies the question/sentence using the NaiveBayes algorithm
    2. Based on the intent it gets response from the corresponding Adapter
    """
    def __init__(self):
        self.math_adapter = MathAdapter()
        self.chatter_adapter = ChatterAdapter()
        self.math_processor = MathProcessor()

    def classify_intent(self, sentence):
        """Classifies the intent in two types
        1. compute - determines that the sentence requires something to be computed
        2. converse - determines that the sentence requires no computations.

        sentence - (str) Inputs a sentence in Natural Language
        """
        tagged_words = nltk.pos_tag(word_tokenize(sentence))
        num_tagged_cd = len([tag for word, tag in tagged_words if tag == 'CD'])
        intent = None
        if num_tagged_cd:
            intent = 'compute'
        else:
            intent = 'converse'
        return intent

    def get_response(self, question):
        """Gets the response from the Adapters bases on their intent.

        question - (str) Inputs a question in natural language
        """
        sentences = sent_tokenize(question)
        responses = []
        for sentence in sentences:
            sentence = self.math_processor.transform_text(sentence)
            intent = self.classify_intent(sentence)
            if intent == 'compute':
                response = self.math_adapter.respond(sentence)
                responses.append(response)
            else:
                response = self.chatter_adapter.respond(sentence)
                responses.append(response)
        return ' '.join(responses)

if __name__ == "__main__":
    mathmonk = MathMonk()
    print(mathmonk.get_response("What is 2+3 multiplied by 5 added by 5?"))
    print(mathmonk.get_response("How are you?"))