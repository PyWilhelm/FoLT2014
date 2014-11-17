import nltk

all_words = nltk.corpus.words.words()

lemma = {'2': ['a', 'b', 'c'], '3': ['d', 'e', 'f'], 
         '4': ['g', 'h', 'i'], '5': ['j', 'k', 'l'],
         '6': ['m', 'n', 'o'], '7': ['p', 'q', 'r', 's'],
         '8': ['t', 'u', 'v'], '9': ['w', 'x', 'y', 'z']}

input_list = ['43556','73837','4','26','3463']


for input_str in input_list:
    words = [w for w in all_words if len(w) == len(input_str)]
    for index, char in enumerate(input_str):
        words = [w for w in words if w[index] in lemma[char]]      
    print words