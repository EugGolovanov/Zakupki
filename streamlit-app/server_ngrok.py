from pyngrok import ngrok 
from token import token
import os
os.system(f'ngrok authtoken {token}')
url = ngrok.connect(port = 8501)
print(url)
input()
