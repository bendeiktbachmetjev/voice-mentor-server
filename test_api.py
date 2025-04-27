import requests
import os

def test_audio_processing(audio_filename):
    # URL API
    url = 'http://127.0.0.1:5000/process-audio'
    
    # Путь к тестовому аудиофайлу
    audio_file_path = os.path.join('test_files', audio_filename)
    
    # Проверяем существование файла
    if not os.path.exists(audio_file_path):
        print(f"Ошибка: Файл {audio_file_path} не найден")
        print("Пожалуйста, поместите аудиофайл в папку test_files")
        return
    
    try:
        print(f"Отправка файла {audio_filename} на сервер...")
        
        # Отправляем POST-запрос с аудиофайлом
        with open(audio_file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            response = requests.post(url, files=files)
        
        # Проверяем ответ
        if response.status_code == 200:
            print("\nУспешный ответ:")
            result = response.json()
            print("\nТранскрипция:")
            print(result['transcript'])
            print("\nОтвет GPT:")
            print(result['response'])
        else:
            print(f"\nОшибка: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\nПроизошла ошибка: {str(e)}")

if __name__ == '__main__':
    # Список поддерживаемых форматов
    supported_formats = ['.mp3', '.wav', '.ogg', '.m4a']
    
    # Получаем список файлов в папке test_files
    test_files = os.listdir('test_files')
    audio_files = [f for f in test_files if any(f.lower().endswith(ext) for ext in supported_formats)]
    
    if not audio_files:
        print("В папке test_files нет аудиофайлов.")
        print(f"Поддерживаемые форматы: {', '.join(supported_formats)}")
        print("Пожалуйста, поместите аудиофайл в папку test_files")
    else:
        print("Найденные аудиофайлы:")
        for i, file in enumerate(audio_files, 1):
            print(f"{i}. {file}")
        
        if len(audio_files) == 1:
            # Если найден только один файл, используем его
            test_audio_processing(audio_files[0])
        else:
            # Если файлов несколько, предлагаем выбрать
            choice = input("\nВведите номер файла для тестирования: ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(audio_files):
                    test_audio_processing(audio_files[index])
                else:
                    print("Неверный номер файла")
            except ValueError:
                print("Пожалуйста, введите число") 