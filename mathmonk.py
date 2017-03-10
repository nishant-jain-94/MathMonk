import nltk
import numpy as np
from corpus import read_corpus
from util import MathProcessor
from adapters import MathAdapter, ChatterAdapter
from nltk import word_tokenize, sent_tokenize

class MathMonk():
    def __init__(self):
        self.math_adapter = MathAdapter()
        self.chatter_adapter = ChatterAdapter()
        self.math_processor = MathProcessor()

    def classify_intent(self, sentence):
        tagged_words = nltk.pos_tag(word_tokenize(sentence))
        num_tagged_cd = len([tag for word, tag in tagged_words if tag == 'CD'])
        intent = None
        if num_tagged_cd:
            intent = 'compute'
        else:
            intent = 'converse'
        return intent

    def get_response(self, question):
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