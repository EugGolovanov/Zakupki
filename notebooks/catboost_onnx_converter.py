import catboost as cb

cb_model = cb.CatBoostClassifier()
cb_model = cb_model.load_model('okpd2-cat-model-1500-lower.cbm')

cb_model.save_model(
    "catboost_model.onnx",
    format="onnx",
    export_parameters={
        'onnx_domain': 'ai.catboost',
        'onnx_model_version': 1,
        'onnx_doc_string': 'test model for classification',
        'onnx_graph_name': 'CatBoostModel_for_Classification'
    }
)
