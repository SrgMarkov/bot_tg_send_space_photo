import argparse
import requests
from save_pictures import save_picture


def get_spacex_launch_photo(launch_id):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    photos = response.json()['links']['flickr']['original']
    for count, photo in enumerate(photos):
        save_picture(photo, 'images', f'spacex_{count}')


if __name__ == '__main__':
    command_arguments = argparse.ArgumentParser\
        (description='Загрузка картинок с запуска SpaceX. Можно указать аргумент id запуска, по умолчанию - последний. '
                     'Если вернулась ошибка 404 - вероятнее всего фотографии запрашиваемого запуска не делались')
    command_arguments.add_argument('-i', '--id', help='ID Запуска', default='last')
    args = command_arguments.parse_args()
    try:
        get_spacex_launch_photo(args.id)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
