import sklearn_crfsuite
from sklearn_crfsuite import metrics

#PARA ENTRENAR EL SISTEMA CON EL CORPUS:
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]


X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]


crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs', 
    c1=0.1, 
    c2=0.1, 
    max_iterations=100, 
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

# Evaluación por palabra. (Qué tal bien se detectó cada etiqueta)
y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred,  digits=3))

#PARA EVALUAR CON NUESTRO SISTEMA PROPUESTO:

clean_tweet = doubspaceB(tweet_texto)

clean_tweet_NEGS, clean_tweet_noNEGS = StratifiedSplitCleanTweets(document)

for ele in sorted(borrar1, reverse = True):  
    del clean_tweet_NEGS[ele] 
    

capa_test_1 = clean_tweet_noNEGS[0:881] + clean_tweet_NEGS[0:486]
capa_test_2 = clean_tweet_noNEGS[881:1762] + clean_tweet_NEGS[486:972]
capa_test_3 = clean_tweet_noNEGS[1762:2643] + clean_tweet_NEGS[972:1458]
capa_test_4 = clean_tweet_noNEGS[2643:3524] + clean_tweet_NEGS[1458:1944]
capa_test_5 = clean_tweet_noNEGS[3524:4405] + clean_tweet_NEGS[1944:2430]
capa_test_6 = clean_tweet_noNEGS[4405:5286] + clean_tweet_NEGS[2430:2916]
capa_test_7 = clean_tweet_noNEGS[5286:6167] + clean_tweet_NEGS[2916:3402]
capa_test_8 = clean_tweet_noNEGS[6167:7048] + clean_tweet_NEGS[3402:3888]
capa_test_9 = clean_tweet_noNEGS[7048:7929] + clean_tweet_NEGS[3888:4374]
capa_test_10 = clean_tweet_noNEGS[7929:8810] + clean_tweet_NEGS[4374:4858]


capa_reales_1 = BIO_noNEGS[0:881] + BIO_NEGS[0:486]
capa_reales_2 = BIO_noNEGS[881:1762] + BIO_NEGS[486:972]
capa_reales_3 = BIO_noNEGS[1762:2643] + BIO_NEGS[972:1458]
capa_reales_4 = BIO_noNEGS[2643:3524] + BIO_NEGS[1458:1944]
capa_reales_5 = BIO_noNEGS[3524:4405] + BIO_NEGS[1944:2430]
capa_reales_6 = BIO_noNEGS[4405:5286] + BIO_NEGS[2430:2916]
capa_reales_7 = BIO_noNEGS[5286:6167] + BIO_NEGS[2916:3402]
capa_reales_8 = BIO_noNEGS[6167:7048] + BIO_NEGS[3402:3888]
capa_reales_9 = BIO_noNEGS[7048:7929] + BIO_NEGS[3888:4374]
capa_reales_10 = BIO_noNEGS[7929:8810] + BIO_NEGS[4374:4858]

#Eligiendo la capa de evaluación:
Tweet_test = copy.copy(capa_test_6)
reales = capa_reales_6


#Detectamos las negaciónes en la capa de evaluación:

def prediction(Tweet_test):
    POStag = []
    for i in Tweet_test:
        doc = nlp(i)
        emptylist1 = []
        for token in doc:
            out = token.text , token.pos_  
            emptylist1.append(out)
        POStag.append(emptylist1)
    return POStag

trainingT = prediction(Tweet_test)
tweet_pred = [sent2features(s) for s in trainingT]
pred = crf.predict(tweet_pred) 


