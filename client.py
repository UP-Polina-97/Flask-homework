import re
import requests

HOST = ('http://127.0.0.1:5000')
resp = requests.post(f'{HOST}/user', json={
    'username': 'user_1',
    'email': 'user#user.com',
    'password': '1234' 
})

print(resp.status_code)
print(resp.text)