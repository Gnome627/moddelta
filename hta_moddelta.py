import os
import filecmp
import shutil
from easygui import diropenbox
from datetime import datetime
import yaml

version='2.0'

config = None
mdeltaignore = [
    'data\\profiles',
    'data\\editor\\newmap',
    'data\\editor\\DiffMasks',
    'data\\editor\\settings.xml',
    'data\\config.cfg',
    'data\\m3deditor.cfg',
    'data\\gsmed.cfg',
    '.bak\\',
    '.ssl.bak' 
]

try:
    with open('mdelta.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        if 'ignore' in config: mdeltaignore = config['ignore']
except:
    print('🚫 файл конфигурации не найден')


def copy_delta(original_game: str, modded_game: str):
    '''
    modded_game_name - ИМЯ папки, в которой лежит игра с установленной модификацией.
    '''
    modded_game_name = modded_game.split(os.path.sep)[-1]
    destination_dir = f'{datetime.now().strftime("%y-%m-%d-%H%M%S")} {modded_game_name}'
    os.makedirs(destination_dir)
    modded_game_data = f'{modded_game}\\data'
    for root, dir, objects in os.walk(modded_game_data):
        for obj in objects:
            obj_path = f'{root}\\{obj}'
            orig_obj_path = f'{root.replace(modded_game, original_game)}\\{obj}'
            # print(f'Сравнивается {obj_path} и {orig_obj_path}')
            if not any(v in obj_path for v in mdeltaignore) and (not os.path.exists(orig_obj_path) or os.path.exists(orig_obj_path) and not filecmp.cmp(obj_path, orig_obj_path)):
                destination_fullpath = f'{destination_dir}\\{obj_path.split(modded_game_name)[1]}'
                os.makedirs(
                    os.path.dirname(destination_fullpath),
                    exist_ok=True
                )
                shutil.copy2(obj_path, destination_fullpath)
                print(f'    💾 {obj_path.split(modded_game_name)[1]} скопирован!')
    print(f'\n🎉 Файлы модификации успешно сохранены в {destination_dir}')
        
    

print(f'Вас приветствует ♻️   HTA ModDelta ver. {version} \n')
original_game = diropenbox(
    msg = 'Выберите директорию с ИСХОДНОЙ (оригинальной/до модификации) игрой.',
    title = 'Выбор исходной игры'
)
print(f'  🍞 Выбрана исходная директория: {original_game}')
modded_game = diropenbox(
    msg = 'Выберите директорию с МОДИФИЦИРОВАННОЙ игрой.',
    title = 'Выбор модифицированной игры'
)
print(f'  🥐 Сравнение с модификацией: {modded_game}')

copy_delta(original_game, modded_game)
input('Нажмите что угодно для продолжения...')
