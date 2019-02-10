import pandas as  pd
import numpy as np
import xml.etree.ElementTree as e


"""
This module contains methods to clean and load datafiles if needed
and some usefull methods
"""

def load_scores_data(file,columns=None):
    """
    Returns a dataframe of a given csv datafiles

    Parameters
    -----------
    file : str
    columns: list of strings

    Returns
    -----------
    DataFrame
    """
    try:
        if columns:
            return pd.read_csv(file,columns=columns)
        else:
            return pd.read_csv(file)
    except:
        raise FileNotFoundExeption


def load_text_xml(xmlfile):
    """
    Parses an xml file and returns a dataframe

    Parameters
    -----------
    xmlfile : str
    columns: list of strings

    Returns
    -----------
    DataFrame
    """
    try:
        root = e.parse(xmlfile).getroot()
    except:
        raise FileNotFoundExeption
    dict_data = {'id': [],
              'text': []}
    for inst in root.findall('instance'):
        dict_data['id'].append(inst.attrib.get('id'))
        dict_data['text'].append(inst.text)
    return pd.DataFrame(dict_data,columns=['id','text'])



def check_arsenl_data(file):
    """
    takes an arsenl data file and checks for the integrity of the seperation with ','

    Parameters
    -----------
    file : str
    """
    try:
        f = open(file)
    except:
        raise FileNotFoundExeption
    datalist = []
    for l in f:
        datalist.append(len(l.split(';')))
    #each line should contain a list of 12 elements after splitting
    num_lines = len(datalist)
    true_val = num_lines * 12
    assert (sum(datalist) == true_val ),"Error, lines contain more or less than 12 elements per line"
    print('Data Successfully checked !')


def get_emotion_index(emotion):
    """
    Returns the index of the emotion in the list for each word as stored

    Parameters
    -----------
    emotion : str
    """
    if emotion == 'anger':
        return 0
    elif emotion == 'disgust':
        return 1
    elif emotion == 'fear':
        return 2
    elif emotion == 'joy':
        return 3
    elif emotion == 'sadness':
        return 4
    elif emotion == 'surprise':
        return 5
    else:
        print('Emotion does not exist')



def get_emotion_fileindex(emotion):
    """
    Returns the index of the emotion in the arsenl data FileNotFoundExeption

    Parameters
    -----------
    emotion : str
    """
    if emotion == 'anger':
        return 6
    elif emotion == 'disgust':
        return 7
    elif emotion == 'fear':
        return 8
    elif emotion == 'joy':
        return 9
    elif emotion == 'sadness':
        return 10
    elif emotion == 'surprise':
        return 11
    else:
        print('Emotion does not exist')

def check_duplicates_per_pos(file):
    """
    takes an arsenl data file and checks for duplicate words within the pos

    Parameters
    -----------
    file : str
    """
    try:
        f = open(file)
    except:
        raise FileNotFoundExeption

    #read first line
    f.readline()
    #create the list of words in the FileNotFoundExeption
    words = []
    for l in f:
        line_elem = l.split(';')
        words.append(line_elem[2])
    #create a set of all the duplicates
    set_duplicates = set([x for x in words if words.count(x) > 1])
    if len(set_duplicates) > 0:
        print(set_duplicates)
    assert(len(set_duplicates)==0),"We have duplicates in the dataset"
    print('No duplicates found !')



def normalise(emotions_list):
        """
        Normalizes a given list of floats

        Parameters:
        -----------
        emotions_list: list of floats

        (x-min(x)) / (max(x)-min(x))
        """
        a = np.array(emotions_list)

        #checks if we will encounter any nAn
        assert(np.isfinite(a).all() == True),"We encounter a NaN while dividing"

        a = (a-min(a)) / (max(a)-min(a))
        return a.tolist()

def map_binary(emotions_list,thresh):
        """
        Retuns a list of type int with all the values mapped to 0 or 1 based
        on a given threshold

        Parameters:
        -----------
        emotions_list: list of floats
        thresh : float
        """
        a = np.array(emotions_list)
        max_value = np.amax(a)
        a[max_value - a > thresh ] =  0
        a[max_value - a < thresh ] =  1
        l = a.astype(int)
        assert(sum(a>1) ==0), "we have values greater than 1"
        return l.tolist()
