# Identificacion de Negaciones

_Identificación automática de expresiones de negación en un corpus de Twitter en Español._

## Requisitos 📋

_Las librerías utilizadas son:_

```
* xml.etree.ElementTree
* spacy (modelo "es_core_news_lg")
* tabulate
* copy
* sklearn_crfsuite
```
### Instalación de spacy: 

$ python -m spacy download es_core_news_lg  
import spacy  
nlp = spacy.load("es_core_news_lg")

## Ejecutando el código ⚙️

El código está dividido en secciónes...
### Prepocesamiento:
En este documento tiene las funciones utilizadas para el procesamiento de los tweets:  
1) Se extraen las etiquetas de negaciones reales del archivo xml. Y se almacenan en un formato estilo BIO.
2) Se lee cada tweet en texto plano.
2.1) Se eliminan dobles espacios y ocurrencias "\\n".
2.3) Se tokeniza con Spacy.
2.4) Se agrega la etiqueta POStag mediante modulos de Spacy.
3) Se junta el token, la etiqueta POS, el etiquetado real de negaciones y se le da un nuevo formato para poder utilizarlo como información de entrenamiento.
4) El total de tweets se separa en 10 capas, cada una con muestras estratificadas, es decir, la misma proporción de tweets con negación, que sin negación.


---
😊
