import os
import argparse
import requests
from dotenv import load_dotenv
from save_pictures import save_picture


def get_nasa_apod_photo(count):
    load_dotenv()
    nasa_api_token = os.getenv("NASA_API_TOKEN")
    get_parameters = {'api_key': nasa_api_token, 'count': count}
    response = requests.get(f'https://api.nasa.gov/planetary/apod', params=get_parameters)
    response.raise_for_status()
    photos = response.json()
    for count, photo in enumerate(photos):
        save_picture(photo['url'], 'images', f'nasa_APOD_{count}')


if __name__ == '__main__':
    command_arguments = argparse.ArgumentParser\
        (description='Загрузка картинок NASA APOC (Astronomy Picture of the Day). Скрипт загружает астрономические '
                     'картинки дня с сайта NASA. Необходимо указать обязательный параметр count - количество '
                     'загружаемых картинок.')
    command_arguments.add_argument('count', help='Количество фотографий', type=int)
    args = command_arguments.parse_args()
    try:
        get_nasa_apod_photo(args.count)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")