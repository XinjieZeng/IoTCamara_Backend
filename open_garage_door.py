import requests
from configs import GARAGE_CREDENTIAL_URL
from configs import MY_Q_USERNAME
from configs import MY_Q_PASSWORD


def open_garage_door(img):
   security_token = get_security_token()


def get_security_token():
    headers = {'MyQApplicationId': 'JVM/G9Nwih5BwKgNCjLxiFUQxQijAebyyg8QUHr7JOrP+tuPb8iHfRHKwTmDzHOu',
               'ApiVersion': '5.1',
               'BrandId': '2'
               }

    data = {'username': MY_Q_USERNAME, 'password': MY_Q_PASSWORD}

    response = requests.post(GARAGE_CREDENTIAL_URL, data=data, headers=headers)
    return response.content


if __name__ == '__main__':
    open_garage_door("ddd")