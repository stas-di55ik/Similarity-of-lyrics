import nltk
import string
from Tools.scripts.ptags import tags
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Початкова обробка тексту (видалення знаків пунктуації + зменшення регістру)
def start_maching(str):
    str = str.lower()
    for character in string.punctuation:
        str = str.replace(character, '')
    return str

#Пошук іменника серед його потенційних форм (для подальшого повернення у базо-ву форму)
def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

#Пошук дієслова серед його потенційних форм (для подальшого повернення у базо-ву форму)
def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

#Пошук прислівника серед його потенційних форм (для подальшого повернення у базову форму)
def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']

#Пошук прикметника серед його потенційних форм (для подальшого повернення у базову форму)
def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']

#Ідентифікація частини мови слова (прямий перебір серед усіх) та повернення базової форми
def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN


#Конвертація списку в рядок
def listToString(s):
    listToStr=' '.join(map(str, s))
    return listToStr

#Переведення слів рядка у базову форму
def base_words_forms(query):
    tags = nltk.pos_tag(query)
    array1 = []
    for tag in tags:
        wn_tag = penn_to_wn(tag[1])
        l = WordNetLemmatizer().lemmatize(tag[0], wn_tag)
        array1.append(l)
    str1 = listToString(array1)
    return set(word_tokenize(str1))


#Текст для аналізу схожості
X="Any text 1"
Y="Any text 2"

#Початкова обробка тексту (функцію див. вище)
X = start_maching(X)
Y = start_maching(Y)

#Виділення ключових слів (видалення повторів)
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)

#Визначення стоп-слів
sw = stopwords.words('english')
l1 = []
l2 = []

#Видалення стоп-слів
X_set = {w for w in X_list if w not in sw}
Y_set = {w for w in Y_list if w not in sw}

#Повернення слів до базової форми
X_set=base_words_forms(X_set)
Y_set=base_words_forms(Y_set)


#Утворення веектору оброблених слів із двох рядків
rvector = X_set.union(Y_set)
for w in rvector:
    #Чи належить елемент вектора 1-му рядку
    if w in X_set: 
        l1.append(1) #так 
    else:
        l1.append(0) #ні 
    #Чи належить елемент вектора 2-му рядку
    if w in Y_set:
        l2.append(1) #так
    else:
        l2.append(0) #ні

#Виведення тексту після проведення обробки та відповідного вектору
print(X_set)
print(l1)
print(Y_set)
print(l2)

c = 0
#Знаходження подібність, що визначається
#як косинуса кута між векторами,
#тобто добуток векторів, поділений на добуток їх довжин.
for i in range(len(rvector)):
    c += l1[i] * l2[i]
cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
print("Similarity is ", cosine*100, "%")
