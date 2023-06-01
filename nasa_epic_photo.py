import os
import argparse
import requests
import datetime
from dotenv import load_dotenv
from save_pictures import save_picture


def get_nasa_epic_photo(count, token):
    get_parameters = {'api_key': token}
    image_parameters = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params=get_parameters).json()
    for number, parameters in enumerate(image_parameters):
        if number == count:
            break
        image_name = parameters['image']
        image_date = datetime.datetime.fromisoformat(parameters['date']).date().strftime("%Y/%m/%d")
        image_url = requests.get(f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png',
                                 params=get_parameters)
        save_picture(image_url.url, 'images', f'nasa_EPIC_{number}')


if __name__ == '__main__':
    load_dotenv()
    nasa_api_token = os.getenv("NASA_API_TOKEN")
    command_arguments = argparse.ArgumentParser\
        (description='Загрузка картинок NASA EPIC (Earth Polychromatic Imaging Camera). Скрипт загружает фотографии с '
                     'камеры полихроматического изображения Земли с самой последней датой съемки. По умолчанию '
                     'загружаются все фотографии с последней датой, при этом количество можно ограничить, указав '
                     'необязательный параметр count.')
    command_arguments.add_argument('-c', '--count', help='Количество фотографий', type=int, default=1000)
    args = command_arguments.parse_args()
    get_nasa_epic_photo(args.count, nasa_api_token)
