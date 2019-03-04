from data_utils import *
import numpy as np


class Arsel(object):
    '''
    Arsel-Lexicon
    '''

    def __init__(self, adj_file, nouns_file, verbs_file, adv_file):
        """
        loads Arsel datasets and checks arsel datasets

        Parameters:
        -----------
        adj :str Arsenl adjectives data file
        nouns :str Arsenl noun data file
        verbs :str Arsenl verb data file
        adv :str Arsenl adverbs data file
        mapbinary: boolean (default:False) maps each words emotions to [0,1] based on a given threshold between the max and other values
        norm:boolean (default:False) normalizes the emotions for each word between 0 and 1
        threshold :float (default=None) threshold for the binary mapping


        binary calculation based on threshold:
            1  if max(emotion) - emotion < threshold
            0 otherwise

        emotion normalization:
            (x-min(x)) / (max(x)-min(x))
        """

        self.dict_adjs = self._load_dict_pos(adj_file)
        self.dict_advs = self._load_dict_pos(adv_file)
        self.dict_nouns = self._load_dict_pos(nouns_file)
        self.dict_verbs = self._load_dict_pos(verbs_file)
        self.sentence_dataframe = pd.DataFrame({'Word': [], 'Anger': [], 'Disgust': [], 'Fear': [
            ], 'Joy': [], 'Sadness': [], 'Surprise': [], 'Not_Found': [], 'Not_Supported_MADAMIRA': [], 'Not_Supported_POS': []})
        self.not_found_word = 0
        self.not_supported_pos = 0

    def get_emotionScores_sentence(self, sentence, binary=False, norm=False, threshold=0.1):
        """Returns the emotions scores for given sentence in buckwalter form

        Parameters
        ----------
        sent: str
                buckwatler form sentence
        Returns
        -------
        scores: float list
             (indexes: [ANGER,DISGUST,FEAR,JOY,SADNESS,SURPRISE])

        """


        splitted_sentence = sentence.split(' ')
        for buck_word in splitted_sentence:
            Not_Supported_MADAMIRA = 0
            split_word = buck_word.split(';')
            try:
                check_split_buck(split_word)
                word, pos = split_word
                word = clean_word(word)
                # check pos
                em_list = self.get_emotionScores_word(word, pos)
                self.sentence_dataframe.loc[len(self.sentence_dataframe)] = [word] + em_list + \
                           [self.not_found_word, 0, self.not_supported_pos] #adding rows to the dataframe
            except AssertionError:
                #not supported madamira
                Not_Supported_MADAMIRA += 1
                self.sentence_dataframe.loc[len(self.sentence_dataframe)] = [split_word, np.nan, np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan, self.not_found_word, Not_Supported_MADAMIRA, self.not_supported_pos]

            #reset for each sentence
            Not_Supported_MADAMIRA = 0
            self.not_found_word = 0
            self.not_supported_pos=0

        #finding the mean values for the emotions
        mn = list(self.sentence_dataframe.describe().loc['mean'][0:6])
        return self._apply_method(mn, binary, norm, threshold)

    def _apply_method(self, scores, binary, norm, threshold):
        """Short summary.

        Parameters
        ----------
        mapbinary: boolean (default:False)
                    maps each words emotions to [0,1] based on a given threshold between the max and other values
        normalize:boolean (default:False)
                    normalizes the emotions for each word between 0 and 1
        threshold :float (default=None)
                    threshold for the binary mapping
        scores : list
                    emotion scores

        Returns
        -------
        modified_scores :list
            scores modified based on the given method

        """
        modified_scores = scores
        # modifiying  word scores nothing new
        if binary:
            modified_scores = map_binary(scores, threshold)
        elif norm:
            modified_scores = normalise(scores)

        return modified_scores

    def get_emotionScores_word(self, word, pos, binary=False, norm=False, threshold=0.1):
        """
        Returns the emotionsscores for a word

        Parameters:
        -----------
        word : str  (buckwalter form)
        pos : str  {'adv','verb','noun','adj'}

        Returns:
        ----------
        float List (format: [ANGER,DISGUST,FEAR,JOY,SADNESS,SURPRISE])
        """
        try:
            if 'adv' in pos:
                return self._apply_method(self.dict_advs[word], binary, norm, threshold)
            elif 'verb' in pos:
                return self._apply_method(self.dict_verbs[word], binary, norm, threshold)
            elif 'noun' in pos:
                return self._apply_method(self.dict_nouns[word], binary, norm, threshold)
            elif 'adj' in pos:
                return self._apply_method(self.dict_adjs[word], binary, norm, threshold)
            self.not_supported_pos = 1
            return  [np.nan, np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan]

        except KeyError:
            self.not_found_word = 1
            return  [np.nan, np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan,
                                   np.nan]

    def get_emotion(self, word, pos, emotion_title, binary=False, norm=False, threshold=0.1):
        """
        Returns the emotion score for a word by pos and emotion

        Parameters:
        -----------
        word : str  (buckwalter form)
        pos : str  (part of speech for the word)
        emotion_title : str {ANGER,DISGUST,FEAR,JOY,SADNESS,SURPRISE}

        Returns:
        ----------
        float
        """
        return self.get_emotionScores_word(word, pos, binary, norm, threshold)[get_emotion_index(emotion_title)]

    def _load_dict_pos(self, file):
        """
        Returns a dict with words as key and the list of emotions as the values

        Parameters:
        -----------
        file: str

        Returns:
        ----------
        dict[words] :  list of scores
        """
        f = open_file(file)

        data_dict = {}
        # read first line
        f.readline()

        for l in f:
            word_scores = []
            line_elem = l.split(';')
            word = line_elem[2]
            for em in ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']:
                idx = get_emotion_fileindex(em)
                em_score = line_elem[idx]
                if em == 'surprise':
                    em_score = em_score.strip()  # clearning the new character at the end
                word_scores.append(float(em_score))

            data_dict[word] = word_scores

        return data_dict
