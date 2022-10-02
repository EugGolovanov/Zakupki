import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel, PreTrainedTokenizer, PreTrainedTokenizerFast
from pyjarowinkler import distance
import faiss
from copy import deepcopy
import catboost as cb
import time


def get_model_tokenizer(hub_name: str):
    tokenizer = AutoTokenizer.from_pretrained(hub_name)
    model = AutoModel.from_pretrained(hub_name)
    return model, tokenizer


class BertCLS(nn.Module):
    def __init__(self, model, n_classes):
        super(BertCLS, self).__init__()
        self.model = model
        self.fc = nn.Linear(312, n_classes)

    def forward(self, batch):
        return self.fc(self.model(**batch).pooler_output)


def get_embeddings(bert_cls, tokenizer, text):
    tokens = tokenizer(text, padding=True,
                       max_length=300, truncation=True,
                       return_tensors='pt')
    tokens = tokens.to(bert_cls.model.device)
    return bert_cls.model(**tokens).pooler_output.detach().cpu().numpy()


def string_dist(str1, str2):
    return distance.get_jaro_distance(str1, str2,
                                      winkler=True,
                                      winkler_ajustment=True,
                                      scaling=0.2)


def prepare_data(data: pd.DataFrame, min_price=0.0, max_price=float('inf'), inn="", okpd2_code="", countries=[]) -> pd.DataFrame:
    if max_price != 0.0:
        data = data.loc[(data['price'] >= min_price) &
                        (data['price'] <= max_price)]
    if okpd2_code != "":
        data = data.loc[data['okpd2_code'].str.startswith(okpd2_code)]
    if inn != "":
        data = data.loc[data['inn'] == inn]
    if countries != []:
        for c in countries:
            data = data.loc[data['country_code'].str.contains(str(int(c)))]
    return data


def get_search_results(search_request: str, data: pd.DataFrame, index: faiss.IndexFlatIP, bert: BertCLS, tokenizer, cb_model: cb.CatBoostClassifier, min_price=0.0, max_price=float('inf'), inn="", okpd2_code="", countries=[], best=True) -> pd.DataFrame:
    new_data = deepcopy(data)
    new_data = prepare_data(new_data, min_price=min_price, max_price=max_price,
                            inn=inn, okpd2_code=okpd2_code, countries=countries)

    xq = get_embeddings(bert, tokenizer, search_request)

    preds = cb_model.predict(xq)
    faiss.normalize_L2(xq)

    k = 100 if best else 250
    D, I = index.search(xq, k)  # type: ignore # xq shape = (1, d)

    indexes = set(new_data.index)
    selected = [i for i in I[0] if i in indexes]

    faiss_results = new_data.loc[selected].reset_index(
        drop=True)  # type: ignore
    faiss_results['string_dist'] = faiss_results['product_name'].apply(
        lambda x: string_dist(x, search_request))

    faiss_results['same_okpd2_code'] = faiss_results['okpd2_value'].apply(
        lambda x: int(x == preds[0]))

    if best:
        return faiss_results.sort_values(by=['same_okpd2_code', "string_dist"], ascending=[False, False])
    return faiss_results.sort_values(by=['same_okpd2_code', "string_dist"], ascending=[True, True]).head(5)
