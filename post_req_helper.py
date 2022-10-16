import requests

app_url = 'https://img2txt-kzbiulmznq-uc.a.run.app/img2txt/'

def send_post(url, image_path):
    with open(image_path, 'rb') as img:
        files = {'file': (image_path, img, 'multipart/form-data',{'Expires': '0'}) }
        with requests.Session() as s:
            r = s.post(url, files=files, timeout=120)
            print(r.status_code)
            print("Received IMG2TEXT OUTPUT:")
            print(r.text)
    
    return r.text