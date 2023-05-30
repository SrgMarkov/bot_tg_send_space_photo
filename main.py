import os
import requests
import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_file_extension(url):
    file_url_path, file_extension = os.path.splitext(urlparse(url).path)
    return file_extension


def save_picture(url, pathname, name):
    response = requests.get(url)
    response.raise_for_status()
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    with open(f'{pathname}/{name}{get_file_extension(url)}', 'wb') as file:
        file.write(response.content)


def get_spacex_launch_photo(launch_id='last', folder='images'):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    photos = response.json()['links']['flickr']['original']
    for count, photo in enumerate(photos):
        save_picture(photo, folder, f'spacex_{count}')


def get_nasa_apod_photo(count, folder='images'):
    load_dotenv()
    nasa_api_token = os.getenv("NASA_API_TOKEN")
    get_parameters = {'api_key': nasa_api_token, 'count': count}
    response = requests.get(f'https://api.nasa.gov/planetary/apod', params=get_parameters)
    response.raise_for_status()
    photos = response.json()
    for count, photo in enumerate(photos):
        save_picture(photo['url'], folder, f'nasa_APOD_{count}')


def get_nasa_epic_photo(count, folder='images'):
    load_dotenv()
    nasa_api_token = os.getenv("NASA_API_TOKEN")
    get_parameters = {'api_key': nasa_api_token}
    image_info_response = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params=get_parameters).json()
    for number, image_info in enumerate(image_info_response):
        image_name = image_info['image']
        image_date = datetime.datetime.fromisoformat(image_info['date']).date().strftime("%Y/%m/%d")
        image = requests.get(f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png',
                             params=get_parameters)
        save_picture(image.url, folder, f'nasa_EPIC_{number}')
        if count == number + 1:
            break


get_nasa_epic_photo(100, 'NASA_EPIC')