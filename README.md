**UzbekStemmer**

version = 0.2.6

authors = [Maksud Sharipov, Ulugbek Salaev, Allabergan Yuldashev, Jasur Sobirov]

Uzbek Stemmer for Python

The Uzbek stemming algorithm was created by [Maksud Sharipov, Ulugbek Salaev, Allabergan Yuldashev, Jasur Sobirov]. It stems all Uzbek words and it is not included any lexicon.

github url: https://github.com/MaksudSharipov/UzbekStemmer

pypi.org url: https://pypi.org/project/UzbekStemmer/

<code>pip install UzbekStemmer</code>
```
Example:
from UzbekStemmer import UzbekStemmer as uzstem
print(uzstem.UzStemmer('Bolalarimizdanmisizlar'))

Result: "Bola"
```