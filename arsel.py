from data_utils import get_emotion_index,get_emotion_fileindex,normalise,map_binary



class Arsel(object):
    '''
    Arsel-Lexicon
    '''

    def __init__(self,adj_file,nouns_file,verbs_file,adv_file,binary=False,norm=False,threshold=0.1):
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
        self.dict_adjs = self._load_dict_pos(adj_file,binary,norm,threshold)
        self.dict_advs = self._load_dict_pos(adv_file,binary,norm,threshold)
        self.dict_nouns = self._load_dict_pos(nouns_file,binary,norm,threshold)
        self.dict_verbs = self._load_dict_pos(verbs_file,binary,norm,threshold)

    def get_emotionScores(self,word,pos):
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
            if pos == 'adv':
                return self.dict_advs[word]
            elif pos == 'verb':
                return self.dict_verbs[word]
            elif pos == 'noun':
                return self.dict_nouns[word]
            elif pos == 'adj':
                return self.dict_adjs[word]
            else:
                print("Please enter a valid pos : {'adv','verb','noun','adj'} ")
        except KeyError:
            print('Word not found in the given POS')

    def get_emotion(self,word,pos,emotion_title):
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
        return self.get_emotionScores(word,pos)[get_emotion_index(emotion_title)]


    def _load_dict_pos(self,file,binary,norm,threshold):
        """
        Returns a dict with words as key and the list of emotions as the values

        Parameters:
        -----------
        file: str
        mapbinary: boolean (default:False) maps each words emotions to [0,1] based on a given threshold between the max and other values
        normalize:boolean (default:False) normalizes the emotions for each word between 0 and 1
        threshold :float (default=None) threshold for the binary mapping

        Returns:
        ----------
        dict[words] :  list of scores
        """
        try:
            f = open(file)
        except:
            raise FileNotFoundExeption

        data_dict = {}
        #read first line
        f.readline()

        for l in f:
            word_scores = []
            line_elem = l.split(';')
            word = line_elem[2]
            for em in ['anger','disgust','fear','joy','sadness','surprise']:
                idx = get_emotion_fileindex(em)
                em_score = line_elem[idx]
                if em == 'surprise':
                    em_score = em_score.strip() #clearning the new character at the end
                word_scores.append(float(em_score))

            #modifiying  word scores
            if binary:
                    word_scores= map_binary(word_scores,threshold)
            elif norm:
                    word_scores =  normalise(word_scores)

            data_dict[word] = word_scores

        return data_dict
