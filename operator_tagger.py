import nltk
from corpus import read_corpus
from nltk.tag import SequentialBackoffTagger

class OperatorTagger(SequentialBackoffTagger):
    """Extends the SequentialBackOffTagger and tags the Operators present in the sentence. 
    Backed by a Parts of Speech Tagger
    """
    
    def __init__(self, *args, **kwargs):
        SequentialBackoffTagger.__init__(self, *args, **kwargs)
        math_words = read_corpus("math_words", extension="json")
        self.operators = math_words["operator_alias"]
        self.operative_adjectives = math_words["operative_adjectives"]
        print(self.operative_adjectives)
        
    def choose_tag(self, tokens, index, history):
        """Tags all the math operators as Operators an addjectives like 'added by' as Operative Adjective """
        tag = None
        if tokens[index] in self.operators:
            tag = "OPERATOR"
        elif tokens[index] in self.operative_adjectives:
            tag = "OPER_ADJ"
        else:
            tag = nltk.pos_tag([tokens[index]])[0][1]
        return tag