import requests

URL = "http://localhost:8000/preprocess"

def get_response(content):
    file = {
        "content": content
    }
    resp = requests.post(url=URL, json=file) 
    return resp.json()

if __name__=='__main__':
    print(get_response("Patient can examine his own prescription"))