import requests
url = 'http://127.0.0.1:8000/upload/'
name_img = r'C:\Users\rajat\Postman Agent\files\p1.png'
#name_img = r'uploadedImages\p1.png'
# name_img = r'C:\Users\saman\Postman Agent\files\WhatsApp Image 2022-10-14 at 9.13.31 PM.jpeg'
#name_img = r"/home/aakash/Pictures/Screenshot from 2022-02-08 16-36-45.png"

with open(name_img, 'rb') as img:
    files = {'file': (name_img, img, 'multipart/form-data',{'Expires': '0'}) }
    with requests.Session() as s:
        r = s.post(url, files=files)
        print(r.status_code)
        print(r.text)