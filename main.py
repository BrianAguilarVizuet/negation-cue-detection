import xml.etree.ElementTree as ET #Librería para procesar archivos .xml
import spacy #Librería spacy. 
nlp = spacy.load("es_core_news_lg") #Modelo grande en español de Spacy.
from tabulate import tabulate #Para presentar los resultados en tablas.
import copy

##############
# Para extraer las etiquetas reales...

document = ET.parse('CORPUS02__.xml')

texto_bio = BItag(document)
tweet_texto_bio = [tweet for sublist in texto_bio for tweet in sublist]
tweet_limpio_bio = doubspace(tweet_texto_bio)
BIOtags = tokenizeBIO(tweet_limpio_bio)

######################
# Para leer los tweets y dividir el corpus en 10 capas estratificadas. 
document = ET.parse('CORPUS02__.xml')
texto = RawTweet(document)
tweet_texto = [tweet for sublist in texto for tweet in sublist]
dic = TokenizeD(document)
list_of_lists = [[list(tup) for tup in elem] for elem in dic]
BIO_NEGS, BIO_noNEGS = StratifiedShuffleSplitA(document)   #Parte A
Listas_NEGS, Listas_noNEGS = StratifiedShuffleSplitB(document) #Parte B

#LIMPIEZA DE TWEETS POBREMENTE LEÍDOS:
borrar1 = []
for y in range(0,len(BIO_NEGS)):
    if len(BIO_NEGS[y]) != len(Listas_NEGS[y]):
        borrar1.append(y)
    
    
for ele in sorted(borrar1, reverse = True):  
    del BIO_NEGS[ele] 
    
for ele in sorted(borrar1, reverse = True):  
    del Listas_NEGS[ele] 
    
#Para (A_nonegs con B_nonegs)...
flat_list_nonegs = [[item for sublist1 in sublist2 for item in sublist1] for sublist2 in Listas_noNEGS]
empt = []
for i in range(len(flat_list_nonegs)):
    a = flat_list_nonegs[i]
    b = BIO_noNEGS[i]
    a[2::3] = b[0::1]
    empt.append(a)
composite_list_nonegs = [[lis[x:x+3] for x in range(0, len(lis),3)] for lis in empt]
nested_lst_of_tuples_nonegs = [[tuple(l) for l in elem] for elem in composite_list_nonegs]



#Para (A_negs con B_negs)...
flat_list_negs = [[item for sublist1 in sublist2 for item in sublist1] for sublist2 in Listas_NEGS]
empt = []
for i in range(len(flat_list_negs)):
    a = flat_list_negs[i]
    b = BIO_NEGS[i]
    a[2::3] = b[0::1]
    empt.append(a)
composite_list_negs = [[lis[x:x+3] for x in range(0, len(lis),3)] for lis in empt]
nested_lst_of_tuples_negs = [[tuple(l) for l in elem] for elem in composite_list_negs]


#De esta manera tenemos separado y con el formato buscado, los tweets con negs y los tweets sin negs
Tweet_No_NEGS = copy.copy(nested_lst_of_tuples_nonegs)
Tweet_NEGS = copy.copy(nested_lst_of_tuples_negs)

#Lo que sigue es dividir el corpus en 10 capas tomando muestras estratificadas:

capa_1 = Tweet_No_NEGS[0:881] + Tweet_NEGS[0:486]
capa_2 = Tweet_No_NEGS[881:1762] + Tweet_NEGS[486:972]
capa_3 = Tweet_No_NEGS[1762:2643] + Tweet_NEGS[972:1458]
capa_4 = Tweet_No_NEGS[2643:3524] + Tweet_NEGS[1458:1944]
capa_5 = Tweet_No_NEGS[3524:4405] + Tweet_NEGS[1944:2430]
capa_6 = Tweet_No_NEGS[4405:5286] + Tweet_NEGS[2430:2916]
capa_7 = Tweet_No_NEGS[5286:6167] + Tweet_NEGS[2916:3402]
capa_8 = Tweet_No_NEGS[6167:7048] + Tweet_NEGS[3402:3888]
capa_9 = Tweet_No_NEGS[7048:7929] + Tweet_NEGS[3888:4374]
capa_10 = Tweet_No_NEGS[7929:8810] + Tweet_NEGS[4374:4858]

# De esta manera en cada iteración se entrena con 9 de las capas
# y se entrena con la capa restante  
train_sents = capa_1 + capa_2 + capa_3 + capa_4 + capa_5 + capa_7 + capa_8 + capa_9 + capa_10
test_sents = capa_6
