## Как запустить локально (on Windows)

Для начала сконируйте репозиторий

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
```
gdown 'https://drive.google.com/uc?id=1h9SvDOcJqEN7Ee-lBSoAOCuHxVxDHD8P'
gdown 'https://drive.google.com/uc?id=1Z5G4HxzjJ9RbV2gU-gn3-GmJz3W9gw9X'
gdown 'https://drive.google.com/uc?id=1F2oq3AFKwE-eWAEvMy9o4NUVQF4whn2_'
gdown 'https://drive.google.com/uc?id=1KYKxZCmLY6d7CW8QFNY1F44iT7cYSDxS'
```
