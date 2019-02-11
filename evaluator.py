from arsel import Arsel
import pandas as pd
from data_utils import *
import csv


class Evaluator(object):
    """
    This class evaluates arsel lexicon

    """
    def __init__(self,arsl):
        """
        intializes an evaluator and loads data required for evaluation
        calculating import metrics.

        Parameters
        ----------
        arsl : Arsel instance

        """
        self.arsel = arsl
        self.dict_buckwalter = {}
        self.dict_scores = {}

    def load(self,file_sentences,file_scores):
        """
        The methods loads the a file with buckwalter sentences and
        another file with the true scores of the sentences by id

        Parameters
        ----------
        file_sentences : str
            file containing bucklwater form sentences in the form of
            id # sentences in buckwalter form
        file_scores : str
            file containing the true scores of the file_sentences in the form of
            id,anger,disgust,fear,joy,sadness,surprise

        """
        buck_sentences = open_file(file_sentences)

        #load ids and buckwalter sentences
        for l in buck_sentences:
            self._check_buck(l)
            split_line = l.split('#')
            self.dict_buckwalter[int(split_line[0])] = split_line[1].strip() #removing new line character


        #load scores converting values to floats
        with open(file_scores) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                self.dict_scores[int(row[0])] = [float(x) for x in row[1:]]



    def _dataframe_data(dict_data,columns):
        """
        This method takes a dictionary and returns a data frame with the given columns
        Parameters
        ----------
        dict_data : type

        Returns
        -------
        DataFrame

        """
        return pd.DataFrame.from_dict(dict_data,orient='index',columns=columns)


    def _check_buck(self,sentence):
        """
        This methods checks if the buckwalter sentences
        has any discripencies regarding the format of 'id#sentences'


        Parameters
        ----------
        file_sentences : str
        """
        count=0
        for c in sentence:
            if c =='#':
                count+=1
        assert (count == 1) , sentence + ": sentence contains more than one #"
