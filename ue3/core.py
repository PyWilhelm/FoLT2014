from nltk.corpus import udhr
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk import word_tokenize
import string
from numpy import fabs


languages = ['English', 'German_Deutsch', 'French_Francais']
language_base = dict((language, udhr.words(language + '-Latin1')) for language in languages)

# Uebung 3.1.a
def build_language_models(languages, language_base):
    condition = [(language, char.lower()) 
                 for language in languages for word in language_base[language] for char in word]
    return ConditionalFreqDist(condition)

# Uebung 3.1.b
def caculate_manhattan_value_char(lm_cfd, words):
    ascii = 'qwertyuiopasdfghjklzxcvbnm'
    ignores = '.,-`\'""0123456789;?!:'
    sorted_dict = {lang: [w for (w, _) in lm_cfd[lang].most_common(20) if w not in ignores] for lang in lm_cfd.keys()}
    sorted_freq_list = [w for (w, _) in FreqDist([c for word in words for c in word.lower()]).most_common(20) if w not in ignores]
    manhattan_dict = {}
    for lang in sorted_dict.keys():
        distance = 0
        for item in sorted_dict[lang]:
            try:
                distance += float(fabs(sorted_freq_list.index(item) - sorted_dict[lang].index(item))) / \
                            len(sorted_dict[lang]) * \
                            float(float(len(sorted_dict[lang]) - sorted_dict[lang].index(item)) / len(sorted_dict[lang]))
            except:
                distance += float(fabs(sorted_dict[lang].index(item) - len(sorted_freq_list))) / \
                            float(len(sorted_dict[lang])) / \
                            float(float(len(sorted_dict[lang]) - sorted_dict[lang].index(item)) / len(sorted_dict[lang]))
        manhattan_dict[lang] = distance / len(sorted_freq_list)
    return sorted(manhattan_dict.iteritems(), key=lambda item: item[1])



# Uebung 3.1.c
def guess_language(language_model_cfd, text, evaluate_func=caculate_manhattan_value_char):
    test_words = word_tokenize(text)
    manhattan_distances_list = evaluate_func(language_model_cfd, test_words)
    print manhattan_distances_list
    return manhattan_distances_list[0][0]
    

# Uebung 3.1.d  
language_model_cfd = build_language_models(languages, language_base)

text1 = "these functions can return any value, which may or may not be interpretable as a Boolean value. See Comparisons for more information about rich comparisons."
text2 = "Il dispute ses premiers matchs au sein de la Ligue d'Alsace de football, atteint la DH en 1924 et obtient le statut professionnel "
text3 = "Sie moechten die Attraktivitaet Ihres Internet-Portales erhoehen und Ihren Kunden DB-Fahrkarten rund um die Uhr anbieten? Sie moechten Ihr Produktportfolio um Services rund um die Bahn erweitern? Dann arbeiten Sie mit der Deutschen Bahn zusammen und profitieren Sie von unseren attraktiven Angeboten!"

# guess the language by comparing the frequency distributions
print 'guess for english text is', guess_language(language_model_cfd, text1)
print 'guess for french text is', guess_language(language_model_cfd, text2)
print 'guess for german text is', guess_language(language_model_cfd, text3)

