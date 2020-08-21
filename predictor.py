import tensorflow as tf
import keras
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import pandas as pd
import numpy as np
import Bio as bio
import seaborn as sns
from sklearn.cluster import KMeans
from joblib import dump, load

#Function to classify.
#Takes either two strings or two lists of strings.


def GenomeFormatter(genomes, colname="Sequence"):
    dummygenes = pd.read_pickle("./dummy.pkl")
    index = genomes.index
    #Values replaced with dummies:

    #list of valid inputs:
    atcg = ["A", "T", "C", "G"]
    #Splitting into separate columns:
    genomes = pd.DataFrame(genomes[colname].apply(lambda x: x+("0" * (31775-len(x)))))
    genomes = pd.DataFrame(genomes[colname].apply(lambda x: list(x)))
    genomes = pd.DataFrame(genomes[colname].to_list())

    #dropping "noise" from sequencing:
    genomes[~genomes.isin(atcg)] = None
    genomes.fillna(0, inplace = True)

    #replacing each nucleotide with its respective dummy value:
    for n in range(0, len(atcg)):
        genomes.replace(atcg[n], (n+1), inplace = True)

    #Filling extra space in with kmeans.expected_n_features with 0.
    #TODO: truncate if it's too long.
    genomes.index = index
    appended = pd.concat([dummygenes.head(0), genomes]).fillna(0)
    return genomes

#Function to classify.
#Takes either two strings or two lists of strings.
def FastaReader(fastafile):
    from Bio import SeqIO
    with open(fastafile) as fasta_file:  # Will close handle cleanly
        identifiers = []
        lengths = []
        seqs = []
        for seq_record in SeqIO.parse(fasta_file, 'fasta'):  # (generator)
            identifiers.append(seq_record.id)
            seqs.append(seq_record.upper().seq)
        df = pd.DataFrame(identifiers)
        df["Sequence"] = seqs
        df.index = df[0]
        df.drop(columns = 0, inplace = True)
    return df

#Takes dataframe from CoronaClass and returns dataframe of cluster
#TODO: Return 5 closest matches.
#Takes a filepath containing fasta-formatted genomes and returns classifications for each:
def CoronaSample():
    coronamodel = load('coronamodel.joblib')
    #Reading file from fasta format into dataframe
    df = FastaReader('test.txt')

    #Formatting for Kmeans:
    formatted = GenomeFormatter(df)
    formatted.drop(columns = 0, inplace = True)

    #Classify input genomes:
    result = coronamodel.predict(formatted.apply(lambda x: list(x)))

    return result

def CoronaClassifier(filepath):
    coronamodel = load('coronamodel.joblib')
    #Reading file from fasta format into dataframe
    df = FastaReader(filepath)

    #Formatting for Kmeans:
    formatted = GenomeFormatter(df)
    formatted.drop(columns = 0, inplace = True)

    #Classify input genomes:
    result = coronamodel.predict(formatted.apply(lambda x: list(x)))

    return result
