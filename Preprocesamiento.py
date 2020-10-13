import xml.etree.ElementTree as ET #Librería para procesar archivos .xml
import spacy #Librería spacy. 
nlp = spacy.load("es_core_news_lg") #Modelo grande en español de Spacy.
from tabulate import tabulate #Para presentar los resultados en tablas.
import copy 

def BItag(document):
    tweet=[]
    for item in document.iter('tweet'):
        dic={}
        tagJer=[]
        tails=[]
        texts=[]
        for node in item.iter('content'):
            if node.text != None:
                dic[node.tag]=node.text
                texts.append(node.text)
            for elem in node.iter():
                if elem.tag == "negexp" and elem.get('class') == "simple" :
                    doc = nlp(elem.text)
                    elem.text = "NEG " * len(doc)
                if elem.tag == "negexp" and elem.get('class') == "related" or elem.get('class') == "no_neg"  :
                    doc = nlp(elem.text)
                    elem.text = "I " * len(doc)
                if elem.tag == "neg_structure" and elem.text != None:
                    doc = nlp(elem.text)
                    elem.text = "I " * len(doc)
                if elem.tag == "event" and elem.text != None:
                    doc = nlp(elem.text)
                    #print(doc, len(doc))
                    elem.text = "I " * len(doc)
                if elem.tag == "event" and elem.tail != None:
                    doc = nlp(elem.tail)
                    #print(doc,len(doc))
                    elem.tail = "I " * (len(doc)-1)
                if elem.get('class') != None:
                    tag=elem.tag+' '+elem.get('class')
                else:
                    tag = elem.tag
                tagJer.append(tag)
                if not elem.tag==node.tag: 
                    if not elem.text == None:
                        dic[tag]=elem.text
                        texts.append(elem.text)
                    if not elem.tail == None:
                        tails.append(elem.tail)
                else:
                    tails.append('')
        tails.reverse()
        for x in tails:
            if x != ' ':
                texts.append(x)
                p = ' '.join(texts)
        tweet.append(p)
        tweets = [tweet[i:i+1] for i in range(0, len(tweet), 1)]
    return tweets


def doubspace(tweet_texto_bio):
    b=[]
    d=[]
    for i in tweet_texto_bio:
        a = i.replace("\\n", " ")
        b.append(a)
        for j in b:
            c = ' '.join(j.split())
        d.append(c)
    return d

def tokenizeBIO(tweet_limpio_bio):
    BIOtag = []
    #emptylist1 = []
    for i in tweet_limpio_bio:
        emptylist1 = []
        doc = nlp(i)
        for token in doc:
            out = token.text 
            emptylist1.append(out)
        BIOtag.append(emptylist1)
    BIOtags = [['O' if j!='NEG' else j for j in i] for i in BIOtag]
    return BIOtags

def RawTweet(document):
    tweet=[]
    for item in document.iter('tweet'):
        dic={}
        tagJer=[]
        tails=[]
        texts=[]
        for node in item.iter('content'):
            if node.text != None:
                dic[node.tag]=node.text
                texts.append(node.text)
            for elem in node.iter():
                if not elem.get('class') == None:
                    tag=elem.tag+' '+elem.get('class')
                else:
                    tag = elem.tag
                tagJer.append(tag)
                if not elem.tag==node.tag:
                    #print(elem.tag,elem.get('class'),elem.text,elem.tail)
                    if not elem.text == None:
                        dic[tag]=elem.text
                        texts.append(elem.text)
                    if not elem.tail == None:
                        tails.append(elem.tail)
                else:
                    tails.append('')
        #print(tagJer)
        #print(dic)
        #print(texts)
        #print(tails)
        tails.reverse()
        for x in tails:
            if x != ' ':
                texts.append(x)
                p = ' '.join(texts)
        tweet.append(p)
        tweets = [tweet[i:i+1] for i in range(0, len(tweet), 1)]
    return tweets


def doubspaceB(tweet_texto):
    b=[]
    d=[]
    #texto = RawTweet(document)
    #tweet_texto = [tweet for sublist in texto for tweet in sublist]
    for i in tweet_texto:
        a = i.replace("\\n", " ")
        b.append(a)
        for j in b:
            c = ' '.join(j.split())
        d.append(c)
    return d

def TokenizeD(document):
    tweet_limpio = doubspaceB(tweet_texto)
    POStag = []
    for i in tweet_limpio:
        doc = nlp(i)
        emptylist1 = []
        for token in doc:
            out = token.text , token.pos_, "BIO"   
            emptylist1.append(out)
        POStag.append(emptylist1)
    return POStag

#Este lo utilizamos para identificar las negaciónes reales y dividir el set en dos, los tweets que tienen al menos una negacion y los tweet que no tienen ni una negacion
def negXML(text):
    lis =[]
    for item in document.iter('tweet'):
        negs =[]
        for node in item.iter('content'):
            for elem in node.iter():
                if elem.tag == "negexp":  
                    negs.append(elem.text)
        lis.append(negs)
    return lis

def StratifiedShuffleSplitA(document):
    BIO_NEGS = copy.copy(BIOtags)
    BIO_noNEGS = copy.copy(BIOtags)
    True_negations = negXML(document)
    borrar_negs = []
    #Eliminamos los tweets que no tienen negaciónes para dividir el data set en dos estratos. (con y sin negación): 
    for y in range(0,13705):
        if len(True_negations[y]) == 0: #No tienen negaciónes, (los borramos y nos quedamos con los que sí tienen)
            borrar_negs.append(y)
    for ele in sorted(borrar_negs, reverse = True):
        del BIO_NEGS[ele]
    #Eliminamos los tweets que tienen al menos una negación.
    borrar_nonegs = []
    for y in range(0,13705):
        if len(True_negations[y]) != 0: #Tienen negaciónes, (los borramos y nos quedamos con los que no tienen)
            borrar_nonegs.append(y)
    for ele in sorted(borrar_nonegs, reverse = True):  
        del BIO_noNEGS[ele]
    return BIO_NEGS, BIO_noNEGS


def StratifiedShuffleSplitB(document):
    Listas_NEGS = copy.copy(list_of_lists)
    Listas_noNEGS = copy.copy(list_of_lists)
    True_negations = negXML(document)
    borrar_negs = []
    #Eliminamos los tweets que no tienen negaciónes para dividir el data set en dos estratos. (con y sin negación): 
    for y in range(0,13705):
        if len(True_negations[y]) == 0: #No tienen negaciónes, (los borramos y nos quedamos con los que sí tienen)
            borrar_negs.append(y)
    for ele in sorted(borrar_negs, reverse = True):
        del Listas_NEGS[ele]
    #Eliminamos los tweets que tienen al menos una negación.
    borrar_nonegs = []
    for y in range(0,13705):
        if len(True_negations[y]) != 0: #Tienen negaciónes, (los borramos y nos quedamos con los que no tienen)
            borrar_nonegs.append(y)
    for ele in sorted(borrar_nonegs, reverse = True):  
        del Listas_noNEGS[ele]
    return Listas_NEGS, Listas_noNEGS


def StratifiedSplitCleanTweets(document):
    clean_tweet_NEGS = copy.copy(clean_tweet)
    clean_tweet_noNEGS = copy.copy(clean_tweet)
    True_negations = negXML(document)
    borrar_negs = []
    #Eliminamos los tweets que no tienen negaciónes para dividir el data set en dos estratos. (con y sin negación): 
    for y in range(0,13705):
        if len(True_negations[y]) == 0: #No tienen negaciónes, (los borramos y nos quedamos con los que sí tienen)
            borrar_negs.append(y)
    for ele in sorted(borrar_negs, reverse = True):
        del clean_tweet_NEGS[ele]
    #Eliminamos los tweets que tienen al menos una negación.
    borrar_nonegs = []
    for y in range(0,13705):
        if len(True_negations[y]) != 0: #Tienen negaciónes, (los borramos y nos quedamos con los que no tienen)
            borrar_nonegs.append(y)
    for el in sorted(borrar_nonegs, reverse = True):  
        del clean_tweet_noNEGS[el]
    return clean_tweet_NEGS, clean_tweet_noNEGS



