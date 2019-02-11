import numpy as np



class Buckwalter(object):
    """
    This class represents a buckwalter sentence as an object.
    Contains methods that will help to manipulate and return information
    about the sentences.
    """
    def __init__(self,sentence):
        """
        Intializes a buckwalter object

        Parameters
        ----------
        sentence : str
            Sentence in buckwalter form
        """
        self.verb_count = 0
        self.noun_count = 0
        self.adjective_count =0
        self.adverb_count = 0
        self.word_count = 0
        self.buck_sentence = sentence
        self.buck_dict = {} #each words mapped to its pos
