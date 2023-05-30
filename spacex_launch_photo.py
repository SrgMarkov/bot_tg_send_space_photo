import argparse
import requests
from save_pictures import save_picture


def get_spacex_launch_photo(launch_id, folder):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    photos = response.json()['links']['flickr']['original']
    for count, photo in enumerate(photos):
        save_picture(photo, folder, f'spacex_{count}')


if __name__ == '__main__':
    command_arguments = argparse.ArgumentParser\
        (description='Загрузка картинок с запуска SpaceX. Можно указать аргумент id запуска и папку для сохранения '
                     'картинок. По умолчанию папка для сохранения - images, запуск - последний. Если вернулась ошибка '
                     '404 - вероятнее всего фотографии запрашиваемого запуска не делались или сервис не доступен')
    command_arguments.add_argument('-i', '--id', help='ID Запуска', default='last')
    command_arguments.add_argument('-f', '--folder', help='Папка для сохранения', default='images')
    args = command_arguments.parse_args()
    try:
        get_spacex_launch_photo(args.id, args.folder)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
