import pandas as pd
import numpy as np
from yaml import load
import utils as utils
import torch
import faiss
import catboost as cb
import onnxruntime as rt
import matplotlib.pyplot as plt

import streamlit as st
import st_aggrid as st_agg


@st.cache(allow_output_mutation=True)
def load_all():
    countries_codes = pd.read_csv('country_directory.csv')
    country2code = dict(
        countries_codes[["country_name", "country_iso_code"]].values)
    
    code2country = dict(
        countries_codes[["country_iso_code", "country_name"]].values)

    model, tokenizer = utils.get_model_tokenizer("cointegrated/rubert-tiny2")
    device = torch.device('cpu')

    bert_cls = utils.BertCLS(model, 1463)
    bert_cls.load_state_dict(torch.load(
        "BertCLS_epoch_2_1500_lower.pth", map_location=torch.device("cpu")))
    bert_cls = bert_cls.to(device)

    final_df = pd.read_feather(
        "bert-tiny-1500-final-df-lower.feather").dropna(subset=['price'])
    data = final_df[final_df.columns[312:]].reset_index(drop=True)

    embeddings = final_df[final_df.columns[:312]].values.astype(np.float32)
    embeddings = np.ascontiguousarray(embeddings)

    faiss.normalize_L2(embeddings)

    d = 312  # длина эмбеддинга
    index = faiss.IndexFlatIP(d)
     # сами эмбеддинги, нампай массив shape = (n_samples, d)
    index.add(embeddings) # type: ignore

    # default catboost
    # cb_model = cb.CatBoostClassifier()
    # cb_model = cb_model.load_model('okpd2-cat-model-1500-lower.cbm')

    # onnx catboost
    cb_model = rt.InferenceSession('catboost_model.onnx')

    return countries_codes, country2code, code2country, tokenizer, bert_cls, data, index, cb_model


def get_fig_price(series: pd.Series):
    data = {"11-20": series[(series.quantile(0.11) <= series) & (series <= series.quantile(0.2))].mean(),
            "21-30": series[(series.quantile(0.21) <= series) & (series <= series.quantile(0.3))].mean(),
            "31-40": series[(series.quantile(0.31) <= series) & (series <= series.quantile(0.4))].mean(),
            "41-50": series[(series.quantile(0.41) <= series) & (series <= series.quantile(0.5))].mean(),
            "51-60": series[(series.quantile(0.51) <= series) & (series <= series.quantile(0.6))].mean(),
            "61-70": series[(series.quantile(0.61) <= series) & (series <= series.quantile(0.7))].mean(),
            "71-80": series[(series.quantile(0.71) <= series) & (series <= series.quantile(0.8))].mean(),
            "81-90": series[(series.quantile(0.81) <= series) & (series <= series.quantile(0.9))].mean(), }
    courses = list(data.keys())
    values = list(data.values())
    plt.style.use('dark_background')  # type: ignore
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses, values, width=0.4)
    ax.bar_label(ax.containers[0])  # type: ignore
    plt.xlabel("Quantile Group")
    plt.ylabel("Price")
    plt.title("Распределение средней цены по квантилям")
    plt.axhline(y=(data['11-20'] + data['81-90']) / 2,
                linewidth=3, color='red', label="Средняя цена", ls="--")
    plt.axhline(y=series.median(), linewidth=3, color='pink',
                label="Медианная цена", ls="--")
    plt.legend()

    return fig

def get_fig_tops(series: pd.Series):
    plt.style.use('dark_background')  # type: ignore
    fig, ax = plt.subplots(figsize=(7, 3))
    counts = series.value_counts()[:5]
    counts = counts / len(series) * 100
    counts.plot(ax = ax, kind = 'barh', xlabel = 'Процент предложений выставленных этим ИНН от общего числа')
    ax.bar_label(ax.containers[0])  # type: ignore
    return fig


def main():
    st.set_page_config(page_title='Zakupki Search Engine')
    st.markdown("""
    # Zakupki Search Engine 
    """)
    countries_codes, country2code, code2country, tokenizer, bert_cls, data, index, cb_model = load_all()
    search_request = st.text_input('Введите слова для поиска:')
    search_expander = st.expander('Дополнительные настройки')
    min_price = search_expander.number_input('Введите минимальную стоимость')
    max_price = search_expander.number_input('Введите максимальную стоимость')
    if max_price < min_price:
        min_price, max_price = max_price, min_price
    inn = search_expander.text_input('Введите ИНН')
    okpd2_code = search_expander.text_input('Введите ОКПД2 код')
    countries = search_expander.multiselect('Выберите страны', countries_codes)
    for i in range(len(countries)):
        countries[i] = country2code[countries[i]]
    if search_request:
        search_request = search_request.strip().lower()
        search_results = utils.get_search_results(search_request, data, index=index, bert=bert_cls, tokenizer=tokenizer, cb_model=cb_model,
                                                  min_price=min_price, max_price=max_price,
                                                  inn=inn, okpd2_code=okpd2_code, countries=countries, best=True)
        figs_expander = st.expander("Анализ рынка")
        fig = get_fig_price(search_results['price'])
        if fig is not None:
            figs_expander.pyplot(fig)
        fig = get_fig_tops(search_results['inn'])
        if fig is not None:
            figs_expander.pyplot(fig)
        search_results.drop(['okpd2_value', 'text', 'string_dist'], axis=1, inplace=True)
        gb_main = st_agg.GridOptionsBuilder.from_dataframe(search_results)
        gb_main.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, editable=False)
        gb_main.configure_side_bar()
        gb_main.configure_selection('single', use_checkbox=True, )
        gb_main.configure_pagination(
            paginationPageSize=10, paginationAutoPageSize=False)
        gb_main.configure_grid_options(domLayout='normal')
        grid_main_options = gb_main.build()
        grid_main_response = st_agg.AgGrid(
            search_results,
            gridOptions=grid_main_options,
            width='100%',
            update_mode=st_agg.GridUpdateMode.MODEL_CHANGED,
            data_return_mode=st_agg.DataReturnMode.AS_INPUT,
            key='main',
            reload_data=True,
        )
        selected_main_row = grid_main_response['selected_rows']
        if len(selected_main_row) != 0:
            info_expander = st.expander('Полная информация')
            country_codes = selected_main_row[0]['country_code'].split('|')
            specs = selected_main_row[0]['product_characteristics'].replace('||', '<br/>')
            for i in range(len(country_codes)):
                if float(country_codes[i]) in code2country:
                    country_codes[i] = code2country[float(country_codes[i])]
                else:
                    country_codes[i] = ""
            info_expander.markdown(f"""
                Наименование товара: {selected_main_row[0]['product_name']}

                Цена: {selected_main_row[0]['price']} ₽

                Единица измерения: {selected_main_row[0]['product_msr']}

                Налогообложение: {selected_main_row[0]['product_vat_rate']}

                Характеристики: <br/>{specs}
                

                ОКПД2  Код: {selected_main_row[0]['okpd2_code']}

                ОКПД2 Наименование: {selected_main_row[0]['okpd2_name']}

                ИНН Поставщика: {selected_main_row[0]['inn']}

                Страна производитель: {", ".join(country_codes)}
            """, unsafe_allow_html=True)
            recommend_results = utils.get_search_results(selected_main_row[0]['product_name'].strip(
            ).lower(), data, index=index, bert=bert_cls, tokenizer=tokenizer, cb_model=cb_model, best=False)
            recommend_results.drop(['okpd2_value', 'text', 'string_dist'], axis=1, inplace=True)
            gb_rec = st_agg.GridOptionsBuilder.from_dataframe(search_results)
            gb_rec.configure_default_column(
                groupable=True, value=True, enableRowGroup=True, editable=False)
            gb_rec.configure_side_bar()
            gb_rec.configure_selection('single', use_checkbox=False, )
            gb_rec.configure_pagination(
                paginationPageSize=10, paginationAutoPageSize=False)
            gb_rec.configure_grid_options(domLayout='normal')
            grid_rec_options = gb_rec.build()
            st.markdown("""
            ### Сопутствующие товары
            """)
            grid_rec_response = st_agg.AgGrid(
                recommend_results,
                gridOptions=grid_rec_options,
                width='100%',
                update_mode=st_agg.GridUpdateMode.MODEL_CHANGED,
                data_return_mode=st_agg.DataReturnMode.AS_INPUT,
                key='rec',
                reload_data=True,
            )


if __name__ == '__main__':
    main()
