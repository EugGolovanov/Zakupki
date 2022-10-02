## Как запустить локально (on Windows)

Для начала сконируйте репозиторий

```
git clone https://github.com/EugGolovanov/Zakupki.git
cd Zakupki
```

Создайте окружения и загрузите библиотеки (python 3.9)

```
cd streamlit-app
python3 -m venv venv
venv\Scripts\activate
pip install gdown
pip install -r requirements.txt
