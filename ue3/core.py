from nltk.corpus import udhr
from nltk.probability import FreqDist
from nltk import word_tokenize
import string


languages = ['English', 'German_Deutsch', 'French_Francais']
language_base = dict((language, udhr.words(language + '-Latin1')) for language in languages)

def build_language_models(languages, language_base):
    return {language: FreqDist([w.lower() for w in language_base[language] 
                                if not (len(w)<2 and w not in string.ascii_letters)]) 
            for language in languages}
    
def guess_language(language_model_cfd, text):
    test_words = word_tokenize(text)
    print test_words
    match_times = {l: 0 for l in language_model_cfd.keys()}
    for language in language_model_cfd.keys():
        for word in test_words:
            keywords = language_model_cfd[language].keys()
            if word.lower() in keywords:
                print word
                match_times[language] += 1
    print match_times
    max_res = ('', 0)
    for key in match_times.keys():
        if max_res[1] < match_times[key]:
            max_res = (key, match_times[key])
    return max_res[0]
    
    
language_model_cfd = build_language_models(languages, language_base)

text1 = "Peter had been to the office before they arrived."
text2 = "Si tu finis tes devoirs, je te donnerai des bonbons."
text3 = "Das ist ein schon recht langes deutsches Beispiel."

# guess the language by comparing the frequency distributions
print 'guess for english text is', guess_language(language_model_cfd, text1)
print 'guess for french text is', guess_language(language_model_cfd, text2)
print 'guess for german text is', guess_language(language_model_cfd, text3)

