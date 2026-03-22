import json
from collections import defaultdict
import numpy as np

def load_words_to_array(filename):
    """
    Загружает слова из файла и возвращает их в виде numpy массива
    """
    with open(filename, 'r', encoding='WINDOWS 1251') as f:
        words = [line.strip() for line in f if line.strip()]
    return np.array(words)


class RussianStemmer:
    """
    Реализация стеммера Портера для русского языка
    """
    
    def __init__(self):
        self.vowels = set('аеиоуыэюя')
        
        self.perfective_gerund_group1 = ['в', 'вши', 'вшись']
        self.perfective_gerund_group2 = ['ив', 'ивши', 'ившись', 'ыв', 'ывши', 'ывшись']
        
        self.adjective_endings = [
            'ее', 'ие', 'ые', 'ое', 'ими', 'ыми', 'ей', 'ий', 'ый', 'ой',
            'ем', 'им', 'ым', 'ом', 'его', 'ого', 'ему', 'ому', 'их', 'ых',
            'ую', 'юю', 'ая', 'яя', 'ою', 'ею'
        ]
        
        self.participle_group1 = ['ем', 'нн', 'вш', 'ющ', 'щ']
        self.participle_group2 = ['ивш', 'ывш', 'ующ']
        
        self.reflexive_endings = ['ся', 'сь']
        
        self.verb_group1 = [
            'ла', 'на', 'ете', 'йте', 'ли', 'й', 'л', 'ем', 'н', 'ло', 'но',
            'ет', 'ют', 'ны', 'ть', 'ешь', 'нно'
        ]
        self.verb_group2 = [
            'ила', 'ыла', 'ена', 'ейте', 'уйте', 'ите', 'или', 'ыли', 'ей',
            'уй', 'ил', 'ыл', 'им', 'ым', 'ен', 'ило', 'ыло', 'ено', 'ят',
            'ует', 'уют', 'ит', 'ыт', 'ены', 'ить', 'ыть', 'ишь', 'ую', 'ю'
        ]
        
        self.noun_endings = [
            'а', 'ев', 'ов', 'ие', 'ье', 'е', 'иями', 'ями', 'ами', 'еи',
            'ии', 'и', 'ией', 'ей', 'ой', 'ий', 'й', 'иям', 'ям', 'ием',
            'ем', 'ам', 'ом', 'о', 'у', 'ах', 'иях', 'ях', 'ы', 'ь', 'ию',
            'ью', 'ю', 'ия', 'ья', 'я'
        ]
        
        self.superlative_endings = ['ейш', 'ейше']
        self.derivational_endings = ['ост', 'ость']
        
        self.participle_endings = self.participle_group1 + self.participle_group2
        self.verb_endings = self.verb_group1 + self.verb_group2
        
    def _find_rv(self, word: str) -> int:
        for i, char in enumerate(word):
            if char in self.vowels:
                return i + 1
        return len(word)
    
    def _find_r1(self, word: str) -> int:
        found_vowel = False
        for i, char in enumerate(word):
            if char in self.vowels:
                found_vowel = True
            elif found_vowel:
                return i
        return len(word)
    
    def _find_r2(self, word: str) -> int:
        r1_pos = self._find_r1(word)
        if r1_pos >= len(word):
            return len(word)
        
        found_vowel = False
        for i in range(r1_pos, len(word)):
            if word[i] in self.vowels:
                found_vowel = True
            elif found_vowel:
                return i
        return len(word)
    
    def _remove_ending(self, word: str, endings: list, position: int, 
                       must_follow_a_ia: bool = False, 
                       check_in_rv: bool = True):
        for ending in sorted(endings, key=len, reverse=True):
            if len(ending) > len(word) - position:
                continue
            
            if word.endswith(ending):
                start_pos = len(word) - len(ending)
                if start_pos < position:
                    continue
                
                if check_in_rv and start_pos < position:
                    continue
                
                if must_follow_a_ia and start_pos > 0:
                    prev_char = word[start_pos - 1]
                    if prev_char not in ['а', 'я']:
                        continue
                
                return word[:start_pos]
        return None
    
    def _remove_reflexive(self, word: str, position: int):
        result = self._remove_ending(word, self.reflexive_endings, position)
        if result is not None:
            return result, True
        return word, False
    
    def _remove_adjectival(self, word: str, position: int):
        for participle in sorted(self.participle_endings, key=len, reverse=True):
            if len(participle) > len(word) - position:
                continue
            
            if word.endswith(participle):
                start_pos = len(word) - len(participle)
                if start_pos < position:
                    continue
                
                is_group1 = participle in self.participle_group1
                if is_group1 and start_pos > 0:
                    prev_char = word[start_pos - 1]
                    if prev_char not in ['а', 'я']:
                        continue
                
                temp_word = word[:start_pos]
                adj_result = self._remove_ending(temp_word, self.adjective_endings, position)
                if adj_result is not None:
                    return adj_result, True
        
        adj_result = self._remove_ending(word, self.adjective_endings, position)
        if adj_result is not None:
            return adj_result, True
        
        return word, False
    
    def _remove_verb(self, word: str, position: int):
        result = self._remove_ending(word, self.verb_group1, position, must_follow_a_ia=True)
        if result is not None:
            return result, True
        
        result = self._remove_ending(word, self.verb_group2, position)
        if result is not None:
            return result, True
        
        return word, False
    
    def _remove_noun(self, word: str, position: int):
        result = self._remove_ending(word, self.noun_endings, position)
        if result is not None:
            return result, True
        return word, False
    
    def _undouble_n(self, word: str) -> str:
        if word.endswith('нн'):
            return word[:-1]
        return word
    
    def _remove_superlative(self, word: str, position: int):
        result = self._remove_ending(word, self.superlative_endings, position)
        if result is not None:
            return result, True
        return word, False
    
    def _remove_soft_sign(self, word: str) -> str:
        if word.endswith('ь'):
            return word[:-1]
        return word
    
    def stem(self, word: str) -> str:
        word = word.lower()
        
        if len(word) <= 2:
            return word
        
        rv_pos = self._find_rv(word)
        
        if rv_pos >= len(word):
            return word
        
        stem = word
        changed = False
        
        result = self._remove_ending(stem, self.perfective_gerund_group2, rv_pos)
        if result is not None:
            stem = result
            changed = True
        
        if not changed:
            result = self._remove_ending(stem, self.perfective_gerund_group1, rv_pos,
                                         must_follow_a_ia=True)
            if result is not None:
                stem = result
                changed = True
        
        if changed:
            pass
        else:
            stem, _ = self._remove_reflexive(stem, rv_pos)
            
            stem, found = self._remove_adjectival(stem, rv_pos)
            if not found:
                stem, found = self._remove_verb(stem, rv_pos)
                if not found:
                    stem, _ = self._remove_noun(stem, rv_pos)
        
        if stem.endswith('и'):
            stem = stem[:-1]
        
        r2_pos = self._find_r2(stem)
        result = self._remove_ending(stem, self.derivational_endings, r2_pos,
                                     check_in_rv=False)
        if result is not None:
            stem = result
        
        stem = self._undouble_n(stem)
        
        stem, found = self._remove_superlative(stem, rv_pos)
        if found:
            stem = self._undouble_n(stem)
        
        stem = self._remove_soft_sign(stem)
        
        if not any(c in self.vowels for c in stem):
            return word
        
        return stem


# # Загрузка и группировка
# print("Загрузка слов...")
# words = load_words_to_array('russian.txt')
# print(f"Загружено {len(words)} слов")

# print("\nГруппировка по корням...")
# stemmer = RussianStemmer()
# groups = defaultdict(list)

# for word in words:
#    stem = stemmer.stem(word)
#    groups[stem].append(word)

# print(f"Сформировано {len(groups)} групп")

# # Сохранение в JSON
# print("\nСохранение в JSON...")
# output_data = {}
# for stem, word_list in groups.items():
#    output_data[stem] = sorted(word_list)

# with open('russian_stems.json', 'w', encoding='utf-8') as f:
#    json.dump(output_data, f, ensure_ascii=False, indent=2)

# print("Готово! Результат сохранен в 'russian_stems.json'")