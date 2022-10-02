# Кодовая база для обучения

1) [zakupki_rubert-tiny-2_final.ipynb](https://github.com/EugGolovanov/Zakupki/blob/main/notebooks/zakupki_rubert-tiny-2_final.ipynb) - запускать на кагле
- Код обучения финальной модели эмбеддингов.

- В качестве претрейна берется модель обученная на данных хакатона в задаче MLM ([Masked-Language Modeling](https://towardsdatascience.com/masked-language-modelling-with-bert-7d49793e5d2c)). \
Благодаря этому мы получаем более быструю и стабильную сходимость модели.
- Финальная модель обучается на задаче классификации.\
В качестве классов берутся ОКПД коды из датасета, но не все.\
Только если ОКПД встречается больше 50 раз в наборе данных - это 1463 классов & 1 миллион строк.
- При инференсе модели для получения эмбеддингов в задачах ранжирования имеет смысл брать чекпоинты,\
что только начали сходиться. Зачастую работает лучше, чем последний чекпоинт.

Референс: [TG Post](https://t.me/ai_newz/1294)

Статьи на эту тему:\
[❱❱ On the surprising tradeoff between ImageNet accuracy and perceptual similarity](https://arxiv.org/abs/2203.04946)[Google]\
[❱❱ Inadequately Pre-trained Models are Better Feature Extractors](https://arxiv.org/abs/2203.04668) [Baidu]

2) [catboost_onnx_converter.py](https://github.com/EugGolovanov/Zakupki/blob/main/notebooks/catboost_onnx_converter.py)  - запускать локально
- Короткий код, для конвертации cbm формата модели катбуста в onnx.
- Это придает ускорение при инференсе.

3) [zakupki-catboost.ipynb](https://github.com/EugGolovanov/Zakupki/blob/main/notebooks/zakupki-catboost.ipynb) - запускать на кагле
- Обучение catboost на эмбеддингах модели из пункта 1.

4) [bert_mlm.ipynb](https://github.com/EugGolovanov/Zakupki/blob/main/notebooks/bert_mlm.ipynb) - обучали на кристофари/mlspace
- Обучение MLM модели.
