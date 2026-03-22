import json
from collections import defaultdict
import numpy as np
import korni
import chastii
import time

vopros = input().split()

mass_vopros = []

words_split = vopros

for j in range(len(words_split)):
    if words_split[j] and words_split[j][-1] in [':', ';', ',', '.', '!', '?']:
        words_split[j] = words_split[j][:-1]

print(words_split)

itog_vopros = []

stemmer = korni.RussianStemmer()
groups = defaultdict(list)

for word in words_split:
    stem = stemmer.stem(word)
    groups[stem].append(word)

# Сохранение в JSON
output_data = {}

for stem, word_list in groups.items():
    output_data[stem] = sorted(word_list)

# Проверка существования chastii.itog
if not hasattr(chastii, 'itog'):
    print("Ошибка: chastii.itog не найден")
    exit(1)

k = 0
znach = {}

# Исправлено: корректная итерация по chastii.itog
for i in range(len(chastii.itog)):
    
    current_item = chastii.itog[i]
    
    # Проверка, что current_item является словарем
    if isinstance(current_item, dict):
        for j in output_data:
            if j in current_item:
                if k in znach:
                    znach[k] += len(current_item[j])
                else:
                    znach[k] = len(current_item[j])
    else:
        print(f"Предупреждение: chastii.itog[{i}] не является словарем")
    
    k += 1

def find_all_max_values(dictionary):
    """
    Находит все ключи с максимальным значением
    
    Returns:
        list: список ключей с максимальным значением
        int: максимальное значение
    """
    if not dictionary:
        return [], 0
    
    max_value = max(dictionary.values())
    max_keys = [key for key, value in dictionary.items() if value == max_value]
    
    return max_keys, max_value

def print_paragraph_by_number(paragraphs, number):
    """
    Выводит абзац по его порядковому номеру
    
    Args:
        paragraphs: список абзацев
        number: порядковый номер абзаца (начиная с 1)
    """
    try:
        # Преобразуем номер в индекс (нумерация с 1)
        index = number - 1
        
        if 0 <= index < len(paragraphs):
            print(f"\n{'='*50}")
            print(f"Абзац №{number}:")
            print(f"{'='*50}")
            
            paragraph = paragraphs[index]
            
            # Вывод в зависимости от типа данных
            if isinstance(paragraph, dict):
                for key, value in paragraph.items():
                    print(f"{key}: {value}")
            elif isinstance(paragraph, str):
                print(paragraph)
            elif isinstance(paragraph, list):
                for item in paragraph:
                    print(item)
            else:
                print(paragraph)
            
            print(f"{'='*50}")
        else:
            print(f"Ошибка: Абзаца с номером {number} не существует")
            print(f"Доступные номера: 1 - {len(paragraphs)}")
    
    except Exception as e:
        print(f"Ошибка при выводе абзаца: {e}")

# Получаем результат
max_keys, max_value = find_all_max_values(znach)

print(f"Максимальное значение: {max_value}")
print(f"Ключи с максимальным значением: {max_keys}")

# Выводим абзацы с максимальными значениями
if max_keys and hasattr(chastii, 'dffbdfmvo'):
    for key in max_keys:
        print_paragraph_by_number(chastii.dffbdfmvo, key + 1)  # +1 так как нумерация с 1
else:
    print("Нет данных для вывода")