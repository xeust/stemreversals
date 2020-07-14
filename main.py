import nltk
import os
from deta import App, Deta
from flask import Flask
from words import words
from nltk.stem import LancasterStemmer, SnowballStemmer



app = App(Flask(__name__))

sno = SnowballStemmer('english')
lan = LancasterStemmer()

proj_key = os.environ["PROJ_KEY"]
deta = Deta(proj_key)
reverse_stems = deta.Base("lancaster_stems")


def reversestemmer(word, stemmer):
    variants = []
    stem = stemmer.stem(word)

    for each in words:
        if stemmer.stem(each) == stem:
            variants.append(each)
            
    return {"key": stem, "stem": stem, "words": variants}


def formatted(stem_dict, word):
    return_words = stem_dict
    del return_words["key"]
    return_words["input"] = word
    return return_words

def get_or_make(word, stemmer):
    word = word
    stem = stemmer.stem(word)
    item = reverse_stems.get(stem)

    if item:
        return formatted(item, word)

    to_cache = reversestemmer(word, stemmer)
    reverse_stems.put(to_cache)
    return formatted(to_cache, word)


@app.route('/', methods=["GET"])
def hello_world():
    return "Stemreversals"


@app.route('/<word>', methods=["GET"])
def reverse_stem(word):
    return get_or_make(word, lan)


@app.lib.run()
def reverse_stem_run(event):
    word = event.json.get('word')
    return get_or_make(word, lan)