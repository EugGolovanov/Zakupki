import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)

def searchbyname(wordf, product_name):
  words = lemmatize(wordf)
  correct = []
  for i in range(len(product_name)):
    lemmas = lemmatize(product_name[i])
    for word in words:
      for lemma in lemmas:
        if lemma == word:
          correct.append(i)
          break
        break
  return set(correct)
