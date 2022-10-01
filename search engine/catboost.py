import catboost as cb
import compress_fasttext as ft
ftmdl = ft.models.CompressedFastTextKeyedVectors.load('https://github.com/avidale/compress-fasttext/releases/download/v0.0.1/ft_freqprune_100K_20K_pq_300.bin')
catboost = cb.CatBoostClassifier()
catboost.load_model('catboost_model.cbm')
def predict_proba(sentences, catboost=catboost, ftmdl=ftmdl)
  if len(sentences) == 1 and type(sentences) == str:
    df = pd.DataFrame(data=ftmdl[sentences]).T
  else:
    df = pd.DataFrame(data=[ftmdl[sentence] for sentence in sentences])
  df['text'] = sentences
  pool = cb.Pool(df, text_features='text')
  return catboost.predict_proba(pool)
