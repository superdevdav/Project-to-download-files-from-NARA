import requests
import os

#пусть пользователь сам разрешает удаление файлов
#проверка на обрыв jpg файла
#вывести проценты выполнения скачивания

def get_response():
    years_range = f"{' OR '.join([str(n) for n in range(1953, 1971)])}"
    params = {
        'q': 'Indexes AND to AND Aerial AND Photography' + years_range,
        'limit': LIMIT,
        'available online': True,
        'sourceIncludes': 'naId,title,digitalObjects.objectUrl'
    }
    API_KEY = 'ZkHEi3N5pW1IvFpMRMttx9EEUHoizuj49atOd9ag'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
    return requests.get(f'{url}/records/search?', headers=headers, params=params)


def get_image(img_url):
    '''Получение файла расширения .jpg'''
    years_range = f"{' OR '.join([str(n) for n in range(1953, 1971)])}"
    params = {
        'q': 'Indexes AND to AND Aerial AND Photography' + years_range,
        'limit': LIMIT,
        'available online': True,
        'sourceIncludes': 'naId,title,digitalObjects.objectUrl'
    }
    API_KEY = 'ZkHEi3N5pW1IvFpMRMttx9EEUHoizuj49atOd9ag'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
    res = requests.get(img_url, headers=headers, params=params).content
    return res


def delete_folders_in_directory(dir_path):
    '''Удаление всех папок в директории'''
    files = os.listdir(dir_path)
    for f in files:
        folder_path = os.path.join(dir_path, f)
        try:
            os.rmdir(folder_path)
        except:
            delete_files_in_directory(folder_path)
            os.rmdir(folder_path)


def delete_files_in_directory(dir_path):
    '''Удаление всех файлов в директории'''
    files = os.listdir(dir_path)
    for f in files:
        file_path = os.path.join(dir_path, f)
        os.remove(file_path)


def load_files(obj):
    folder_name = obj['_source']['record']['title']
    dir_path = path + "//Indexes to Aerial Photography"
    image_url = []
    file_name = []
    for elem in obj['_source']['record']['digitalObjects']:
        image_url.append(elem['objectUrl'])
        file_name.append(elem['objectUrl'].split('/')[-1])

    #создание папки, где будут сохраняться файлы .jpg
    try:
        os.mkdir(path + '//Indexes to Aerial Photography//' + folder_name)
    except:
        delete_files_in_directory(path + '//Indexes to Aerial Photography//' + folder_name)
        os.rmdir(path + '//Indexes to Aerial Photography//' + folder_name)
        os.mkdir(path + '//Indexes to Aerial Photography//' + folder_name)

    for i in range(len(image_url)):
        image_data = get_image(image_url[i])
        final_path = f"{dir_path}//{folder_name}//{file_name[i]}"
        with open(final_path, 'wb') as load_file:
            load_file.write(image_data)


current_file_path = os.path.abspath(__file__)
path = os.path.dirname(current_file_path)

try:
    os.mkdir("Indexes to Aerial Photography")
except:
    delete_folders_in_directory(path + '//Indexes to Aerial Photography//')
    os.rmdir("Indexes to Aerial Photography")
    os.mkdir("Indexes to Aerial Photography")


while True:
    try:
        LIMIT = int(input("How many files do you need to download? Enter an integer: "))
        if LIMIT > 0:
            break  # Прерывание цикла, если введено целое число
    except ValueError:
        print("Incorrect input! Enter an integer!")

url = 'https://catalog.archives.gov/api/v2'
response = get_response()
if response.status_code == 200:
    print(f"Will be downloaded {LIMIT} file(s).")
    data = response.json()

    for item in data['body']['hits']['hits']:
        load_files(item)
        print("Files loaded succesfully")

elif response.status_code == 500:
    print("The entered number is more than the number of available files!")
    print(f"Error: {response.status_code}")
else:
    print(f"Error: {response.status_code}")
