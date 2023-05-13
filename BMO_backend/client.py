import requests

files = open('Cyberpunk.png', 'rb')

upload = {'file': files}

res = requests.post(' http://146.56.106.142/uploadfile/', files = upload)
