from nltk.corpus import udhr
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk import word_tokenize
import string
from numpy import fabs


languages = ['English', 'German_Deutsch', 'French_Francais']
language_base = dict((language, udhr.words(language + '-Latin1')) for language in languages)

def build_language_models(languages, language_base):
    condition = [(language, char.lower()) 
                 for language in languages for word in language_base[language] for char in word]
    return ConditionalFreqDist(condition)

def caculate_mann_value(lm_cfd, words):
    ascii = 'qwertyuiopasdfghjklzxcvbnm'
    sorted_dict = {lang: [w for (w, _) in lm_cfd[lang].most_common() if w in ascii] for lang in lm_cfd.keys()}
    print sorted_dict
    sorted_freq_list = [w for (w, _) in FreqDist([c for word in words for c in word.lower()]).most_common() if w in ascii]
    print sorted_freq_list
    manhattan_dict = {}
    for lang in sorted_dict.keys():
        distance = 0
        for item in sorted_freq_list:
            try:
                distance += fabs(sorted_freq_list.index(item) - sorted_dict[lang].index(item))
            except:
                distance += fabs(sorted_freq_list.index(item) - len(sorted_dict[lang]))
        manhattan_dict[lang] = distance
    return sorted(manhattan_dict.iteritems(), key=lambda item: item[1])
    
def guess_language(language_model_cfd, text):
    test_words = word_tokenize(text)
    print test_words
    manhattan_distances_list = caculate_mann_value(language_model_cfd, test_words)
    print manhattan_distances_list
    return manhattan_distances_list[0][0]
    
    
language_model_cfd = build_language_models(languages, language_base)

text1 = "these functions can return any value, which may or may not be interpretable as a Boolean value. See Comparisons for more information about rich comparisons."
text2 = "Il dispute ses premiers matchs au sein de la Ligue d'Alsace de football, atteint la DH en 1924 et obtient le statut professionnel "
text3 = "Sie mchten die Attraktivitt Ihres Internet-Portales erhhen und Ihren Kunden DB-Fahrkarten rund um die Uhr anbieten? Sie mchten Ihr Produktportfolio um Services rund um die Bahn erweitern? Dann arbeiten Sie mit der Deutschen Bahn zusammen und profitieren Sie von unseren attraktiven Angeboten!"

# guess the language by comparing the frequency distributions
print 'guess for english text is', guess_language(language_model_cfd, text1)
print 'guess for french text is', guess_language(language_model_cfd, text2)
print 'guess for german text is', guess_language(language_model_cfd, text3)

