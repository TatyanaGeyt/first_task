from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic

import scipy.stats as stats

print("Choose file (0 or 1):")
print(" >> 0 - 'wordsim_relatedness_goldstandard.txt'")
print(" >> 1 - 'wordsim_similarity_goldstandard.txt'")
MODE = int(input())

FILE = ["wordsim_relatedness_goldstandard.txt", "wordsim_similarity_goldstandard.txt"]
METHOD = ["lch", "wup", "jcn"]
NAME = ["relatedness", "similarity"]

def make_correct_synset(str):
    arr = []
    for synset in wn.synsets(str):
        if (synset.name().split('.')[0] == str and synset.pos() == 'n'):
            arr.append(synset)
    return arr

file = open(FILE[MODE], "r")
brown_ic = wn_ic.ic('ic-brown.dat')

sorted_data = [[], [], []] # to created sorted files
data = [[], [], [], []] # to calculate Spearman's measure

arr_str = file.readline().split()
while arr_str:

    first = make_correct_synset(arr_str[0])
    second = make_correct_synset(arr_str[1])

    score = [-1, -1, -1]

    for synset1 in first:
        for synset2 in second:
            score[1] = max(score[1], round(synset1.wup_similarity(synset2), 4))
            score[0] = max(score[0], round(synset1.lch_similarity(synset2), 4))
            score[2] = max(score[2], round(synset1.jcn_similarity(synset2, brown_ic), 4))

    if score[0] != -1: # checking if the synset is empty
        # if we can apply one of the methods, then we can apply the rest
        data[0].append(float(arr_str[2]))
        for i in range (3):
            sorted_data[i].append([score[i], arr_str[0], arr_str[1]])
            data[i + 1].append(score[i])

    arr_str = file.readline().split()

file.close()

# create sorted files
for i in range (3):
    sorted_data[i].sort(key=lambda x: x[0], reverse=True)
    new_name = NAME[MODE] + '_' + str(METHOD[i]) + ".txt"
    new_file = open(new_name, "w")
    for j in sorted_data[i]:
        new_file.write(j[1] + '    ' + j[2] + '    ' + str(j[0]) + '\n')
    new_file.close()

# calculate Spearman's measure
print("Spearman's measure, " + FILE[MODE] + ':')
for i in range (3):
    rho, p_value = stats.spearmanr(data[0], data[i + 1])
    print(" >> " + METHOD[i] + ': ' + str(round(rho, 4)))
