import json
from collections import defaultdict
import numpy as np
import korni

def load_words_to_array(filename):
    """
    Загружает слова из файла и возвращает их в виде numpy массива
    """
    try:
        with open(filename, 'r', encoding='Windows 1251') as f:
            words = [line.strip() for line in f if line.strip()]
        return np.array(words)
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return np.array([])
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return np.array([])

# Загружаем слова из файла
dffbdfmvo = load_words_to_array('text.txt')
words = load_words_to_array('text.txt')

# Проверка, что слова загружены
if len(words) == 0:
    print("Предупреждение: не удалось загрузить слова из text.txt")
    itog = []
else:
    mass = []

    for i in range(len(words)):
        words_split = words[i].split()

        for j in range(len(words_split)):
            if words_split[j] and words_split[j][-1] in [':', ';', ',', '.', '!', '?']:
                words_split[j] = words_split[j][:-1]
        
        mass.append(words_split)

    itog = []
    for i in range(len(mass)):
        words_list = mass[i]
        
        stemmer = korni.RussianStemmer()
        groups = defaultdict(list)  # Исправлено: убран korni. перед defaultdict

        for word in words_list:
            stem = stemmer.stem(word)
            groups[stem].append(word)

        # Сохранение в JSON
        output_data = {}
        for stem, word_list in groups.items():
            output_data[stem] = sorted(word_list)
        itog.append(output_data)