import numpy as np


class Buckwalter(object):
    """
    Contains methods that will help to manipulate and return information
    about the buckwalter sentences.
    """

    def __init__(self, buckwalter_list, pos_uniq=False):
        """
        Intializes a buckwalter object

        Parameters
        ----------
        buckwalter_list: list of str (sentences) in buckwalter form

        pos_uniq : boolean
                    returns uniq counts

        """
        self.verb_count = 0
        self.noun_count = 0
        self.adjective_count = 0
        self.adverb_count = 0
        self.word_count = 0  # all words including not supported
        self.unsupported_pos_count = 0
        self.unsupported_word = 0
        self.buckwalter_list = buckwalter_list
        # each word mapped to its pos (contains  words found)
        self.buck_dict = {}
        self.unsupported_madamira_list = []
        self.word_uniq_count = 0  # only unique , might contain words from more than 4 pos
        self.pos_uniq = pos_uniq
        self.parse_sentence_list()

    def parse_sentence_list(self):
        """
        parses a sentences and saves information about the Buckwalter
        sentences like
        --------------
        verb count
        noun count
        adv count
        adj count
        word count
        unsupported count
        unsupported pos count

        Parameters
        ----------
        buckwalter_list :
                    list of all the buckwalter sentences
        """
        for sent in self.buckwalter_list:
            splitted_sentence = sent.split(' ')
            for buck_word in splitted_sentence:
                split_word = buck_word.split(';')
                self.word_count += 1
                try:
                    self._check_split_buck(split_word)
                except:
                    # word do not have a buckwalter form
                    self.unsupported_madamira_list.append(split_word)
                    self.unsupported_word += 1  # words that madamira couldnt figure out a pos
                    # empty pos for unsupported words
                    self.buck_dict[split_word[0]] = ''
                    continue

                word, pos = split_word
                word = self._clean_word(word)  # remove -,_

                # check if word+pos is already in the dict
                if self._check_uniq(word, pos) & self.pos_uniq:
                    self.word_uniq_count += 1
                    # checkOS
                    self._update_pos_count(pos)

                if not self.pos_uniq:
                    self._update_pos_count(pos)

                self.buck_dict[word] = pos

    def _check_uniq(self, word, pos):
        """Checks if a word already have been seen with the same tag
        (used for calculating the unique count of words by pos)

        Parameters
        ----------
        word : str
        pos : str

        Returns
        -------
        boolean
            True if a word is uniq  false otherwise
        """
        if word in self.buck_dict.keys():
            if self.buck_dict[word] == pos:
                return False
        return True

    def _update_pos_count(self, pos):
        """This method updates the pos tags based on  uniqueness requirement

        Parameters
        ----------
        pos : str
            word part of speech (noun,verb)

        unique : boolean
        """
        if pos in ['verb', 'noun', 'adj', 'adv']:
            if pos == 'verb':
                self.verb_count += 1
            if pos == 'noun':
                self.noun_count += 1
            if pos == 'adj':
                self.adjective_count += 1
            if pos == 'adv':
                self.adverb_count += 1
        else:
            self.unsupported_pos_count += 1  # punc..etc..

    def _clean_word(self, buck_word):
        """This methods cleans a word if it contained the characters
            '_' and remove '-' from verbs

        Parameters
        ----------
        buck_word : str
            a string representing a word in buckwalter form without the pos tag
        Returns
        -------
        str
            cleaned word str in buckwalter form

        """
        if '_' in buck_word:
            buck_word = buck_word.split('_')[0]

        if '-' in buck_word:
            buck_word = buck_word.replace('-', '')

        assert (not ('_' in buck_word)
                ), "word still contains unwanted characters"
        assert (not ('-' in buck_word)
                ), "word still contains unwanted characters"

        return buck_word

    def sent_stat(self):
        """Returns sentences information
        Parameters
        -------
        uniq_pos boolean
                    keys changed to uniq (better representations)

        Returns
        -------
        dict: with the following keys
        sentence : str
        words_count: int
        verbs_count: int
        noun count: int
        adv count: int
        adj count: int
        unsupported pos count: int
        unsupported count: int
        """
        uns_uniq = 0
        info_list = ['verbs_count', 'nouns_count', 'advs_count', 'adjs_count']
        if self.pos_uniq:
            info1 = ['uniq_' + x for x in info_list]
            verbs_c, nouns_c, advs_c, adjs_c = info1
            uns_uniq = len(self.buck_dict) - self.word_uniq_count
        else:
            verbs_c, nouns_c, advs_c, adjs_c = info_list

        dict_stat = {
            verbs_c: self.verb_count,
            nouns_c: self.noun_count,
            advs_c: self.adverb_count,
            adjs_c: self.adjective_count,
            'words_count': self.word_count,
            'words_uniq': self.word_uniq_count,
            'unsupported_count': self.unsupported_word,
            'unsupported_uniq_count': uns_uniq,
            'unsupported_pos_count': self.unsupported_pos_count}

        return dict_stat

    def _check_split_buck(self, split_buck):
        """
        This method checks whether each buckwalter word is in the form
        of word;pos

        Parameters
        ----------
        split_buck : list

        """
        assert len(split_buck) == 2, "The word has {} elements".format(
            len(split_buck))

    def __str__(self):
        note = ''
        if uniq_pos_counts:
            note = 'NOTE POS COUNTS UNIQUE'
        return "\" {} \"\nword count: {}\nverb count: {}\nnoun count: {}\nadverb count: {}\nadjective count: {}\nunsupported pos count: {}\nunsupported word count: {}\n {}".format(
            self.buck_sentence, self.word_count, self.verb_count, self.noun_count, self.adverb_count, self.adjective_count, self.unsupported_pos_count, self.unsupported_word, note)
