import requests
url = 'http://127.0.0.1:8000/upload/'
name_img = r'C:\Users\rajat\Postman Agent\files\Boston Pic.jpeg'

with open(name_img, 'rb') as img:
    files = {'file': (name_img, img, 'multipart/form-data',{'Expires': '0'}) }
    with requests.Session() as s:
        r = s.post(url, files=files)
        print(r.status_code)
        print(r.text)