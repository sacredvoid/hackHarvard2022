import requests
url = 'http://127.0.0.1:8000/upload/'
files = {'image': open(r'C:\Users\rajat\Postman Agent\files\Boston Pic.jpeg', 'rb')}
resp = requests.post(url, files=files)

name_img = 'try.jpeg'

with open(r'C:\Users\saman\Downloads\WhatsApp Image 2022-10-14 at 9.13.31 PM.jpeg', 'rb') as img:
    files = {'file': (name_img,img,'multipart/form-data',{'Expires': '0'}) }
    with requests.Session() as s:
        r = s.post(url,files=files)
        print(r.status_code)
        print(r.text)