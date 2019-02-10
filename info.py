"""
This module has methods for loading information about the datasets
"""

def view_text_by_results(df_scores,df_sentences,col,func=max):
    """
    Returns one sentence from the given emotion column
    based on a given function for the emotion values

    Parameters:
    ------------
    df_scores: scores DataFrame
    df_sentences : sentences Dataframe
    col : emotion columns
    func {max,'min',..}: function to apply to emotion values (default=max)

    Returns
    ------------
    result : str
    """
    max_value = df_scores.loc[df_scores[col] == func(df_scores[col]),'id'].tolist()[0]
    return df_sentences.loc[df_sentences['id']== str(max_value),'text'].tolist()[0]
