from arsel import Arsel
import pandas as pd
from data_utils import *
import csv
from buckwalter import Buckwalter


class Evaluator(object):
    """
    This class evaluates arsel lexicon and returns information given a list of
    sentences in buckwalter form

    """

    def __init__(self, arsl):
        """
        intializes an evaluator and loads data required for evaluation
        calculating import metrics.

        Parameters
        ----------
        arsl : Arsel instance

        """
        self.arsel = arsl
        self.dict_buckwalter = {}
        self.dict_scores_true = {}
        self.word_list = []  # used to count the number of uniq words
        self.unsupported_madamira_list = []

        self.dataset_stat = {'verbs_count': 0,
                             'nouns_count': 0,
                             'advs_count': 0,
                             'adjs_count': 0,
                             'words_count': 0,
                             'word_uniq_count': 0,
                             'unsupported_count': 0,
                             'unsupported_pos_count': 0,
                             'pos_uniq': False}

    def load(self, file_sentences, file_scores, pos_uniq=False):
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
        self.dataset_stat['pos_uniq'] = pos_uniq

        buck_sentences = open_file(file_sentences)
        list_buckwalter = []
        # load ids and buckwalter sentences
        for l in buck_sentences:
            self._check_buck(l)
            split_line = l.split('#')
            # removing new line character
            list_buckwalter.append(split_line[1].strip())

        self.buck_obj = Buckwalter(list_buckwalter, pos_uniq)
        self.dataset_stat = self.buck_obj.sent_stat()


        # load scores converting values to floats
        with open(file_scores) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                self.dict_scores_true[int(row[0])] = [float(x) for x in row[1:]]



    def buck_obj(self):
        """Returns a Buckwalter Object containing information about the list of buckwalter sentences

        Returns
        -------
        Buckwalter obj

        """
        return self.buck_obj

    def dataset_info(self):
        """Returns a dict containing info about the current dataset

        Returns
        -------
        dict
            dict containing the different stats as keys:
            uniq/verbs_count
            uniq/nouns_count
            uniq/advs_count
            uniq/adjs_count
            words_count
            word_uniq_count
            unsupported_count
            unsupported_uniq_count
            unsupported_pos_count
        """
        # returns the uniq word count that contains everything including the supported and not unsupported
        # and including all pos tags
        return self.dataset_stat

    def _dataframe_data(dict_data, columns):
        """
        This method takes a dictionary and returns a data frame with the given columns
        Parameters
        ----------
        dict_data : type

        Returns
        -------
        DataFrame

        """
        return pd.DataFrame.from_dict(dict_data, orient='index', columns=columns)

    def _check_buck(self, sentence):
        """
        This methods checks if the buckwalter sentences
        has any discripencies regarding the format of 'id#sentences'


        Parameters
        ----------
        file_sentences : str
        """
        count = 0
        for c in sentence:
            if c == '#':
                count += 1
        assert (count == 1), sentence + ": sentence contains more than one #"
