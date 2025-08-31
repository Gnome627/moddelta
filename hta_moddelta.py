import os
import filecmp
import shutil
from datetime import datetime
import yaml

try:
    with open('moddelta_config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
except:
    print('🚫 файл конфигурации не найден')
    input('Нажмите клавишу Any...')
    quit()

def get_dir_entries(get_dirs: bool = True, sub: str = None):
    obj_list = os.listdir(config['base_path'])
    if get_dirs:
        filtered_list = [obj for obj in obj_list if os.path.isdir(f'{config["base_path"]}\\{obj}')]
    else:
        filtered_list = [obj for obj in obj_list if os.path.isfile(f'{config["base_path"]}\\{obj}')]
    if sub == None:
        return(filtered_list)
    else:
        return([dir for dir in filtered_list if sub in dir and not sub == dir])

def select_mod_folder(mod_folders: list[str]):
    while True:
        choosen_mod_folder_number = input('\n🍞 Введите номер директории, содержащей Вашу модификацию: ')
        try:
            numer = int(choosen_mod_folder_number) - 1
            if mod_folders[numer]:
                print(f'  • Выбрана директория: {mod_folders[numer]}')
                return mod_folders[numer]
        except ValueError:
            print('  🚫 неправильный формат ввода!!')


def copy_delta(modded_game_name: str):
    '''
    modded_game_name - ИМЯ папки, в которой лежит игра с установленной модификацией.
    '''
    destination_dir = f'ModDelta {modded_game_name} {datetime.now().strftime("%y-%m-%d-%H%M%S")}'
    os.makedirs(destination_dir)
    modded_game_data = f'{config["base_path"]}\\{modded_game_name}\\data'
    for root, dir, objects in os.walk(modded_game_data):
        for obj in objects:
            obj_fullpath = f'{root}\\{obj}'
            orig_obj_fullpath = obj_fullpath.replace(modded_game_name, config['hta_folder_name'])
            if not any(v in obj_fullpath for v in config['ignore']) and (not os.path.exists(orig_obj_fullpath) or os.path.exists(orig_obj_fullpath) and not filecmp.cmp(obj_fullpath, orig_obj_fullpath)):
                destination_fullpath = f'{destination_dir}\\{obj_fullpath.split(modded_game_name)[1]}'
                os.makedirs(os.path.dirname(destination_fullpath), exist_ok=True)
                shutil.copy2(obj_fullpath, destination_fullpath)
                print(f'    💾 {obj_fullpath.split(modded_game_name)[1]} скопирован!')
    print(f'\n🎉 Файлы модификации успешно сохранены в {destination_dir}')
        
    

print(f'Вас приветствует ♻️   HTA ModDelta ver. {config["version"]} \n')
possible_mod_folders = get_dir_entries(sub = config['hta_folder_name'])

if len(possible_mod_folders) > 1:
    for index, mod in enumerate(possible_mod_folders):
        print(f'{index + 1} • {mod}')
    mod_folder_name = select_mod_folder(possible_mod_folders)
elif len(possible_mod_folders) == 1:
    mod_folder_name = possible_mod_folders[0]
else:
    raw_dir = input('🍞 Введите имя директории, содержащей Вашу модификацию: ')
    if os.path.isdir(f'{config["base_path"]}\\{raw_dir}'):
        print(f'  • Выбрана директория: {raw_dir}')
        mod_folder_name = raw_dir
    else:
        print('🚫 модификации не найдены')
        input('Нажмите клавишу Any...')
        quit()

copy_delta(mod_folder_name)
input('Нажмите что угодно для продолжения...')
