from arsenl import Arsel
import numpy as np
import pandas as np


if __name__ = "__main__":

    adj ='arsel/arsenl_a.txt'
    verb ='arsel/arsenl_v.txt'
    adv = 'arsel/arsenl_r.txt'
    nouns = 'arsel/arsenl_n.txt'
    arsenl = Arsenl(adj,nouns,verb,adv)
