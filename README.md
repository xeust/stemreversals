## Stemreversals

Stemreversals is an api that, given a word, provides a list of words with the same stem (according to a stemming algorithm).

## Use

Make a `GET` request to: 

```
endpoint/:word
```

Stemreversals will respond with

```json
{
  "input": <word>,
  "stem": <word_stem>,
  "words": [<words_with_common_stem>]
}
```

The first time a stem is queried, the calculation is slow-ish (5-6 seconds). 

From this point forwards, the result is cached in a database and is fast.

Currently configured to use the Lancaster stemmer. Snowball is a bit faster but less aggressive.

Built using [flask](https://flask.palletsprojects.com/en/1.1.x/) and [nltk](https://www.nltk.org/), running on [deta](https://www.deta.sh/) (examples using Micros & Base).
