## Как запустить локально (on Windows 11)

Для начала склонируйте репозиторий

```
git clone https://github.com/EugGolovanov/Zakupki.git
cd Zakupki
```

Создайте окружения и загрузите библиотеки (python 3.9.6)

```
cd streamlit-app
python -m venv venv
venv\Scripts\activate
pip install gdown
pip install -r requirements.txt
```

Загрузите данные и веса через gdown (если не получается через него, то загрузите по прямым ссылкам и положите в данную директорию)
```python 3
gdown 'https://drive.google.com/uc?id=1h9SvDOcJqEN7Ee-lBSoAOCuHxVxDHD8P'
gdown 'https://drive.google.com/uc?id=1Z5G4HxzjJ9RbV2gU-gn3-GmJz3W9gw9X'
gdown 'https://drive.google.com/uc?id=1F2oq3AFKwE-eWAEvMy9o4NUVQF4whn2_'
gdown 'https://drive.google.com/uc?id=1KYKxZCmLY6d7CW8QFNY1F44iT7cYSDxS'
```

Для запуска локально
```
streamlit run app.py
```

Для запуска через ngrok создайте файл token.py и вставьте туда ваш токен ngrok по следующему шаблону:
```
token = '11111'
```
Затем выполните следующие команды(в разных колнсолях)
```
python server_ngrok.py
streamlit run --server.port 80 app.py
```
