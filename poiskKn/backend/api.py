# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict
import korni
import chastii
import json

app = Flask(__name__)
CORS(app)  # ????????? CORS ??? ???????? ?? React

class QuestionProcessor:
    """
    ????? ??? ????????? ???????? ? ?????? ??????????????? ???????
    """
    
    def __init__(self):
        self.stemmer = korni.RussianStemmer()
        self.groups = defaultdict(list)
        self.output_data = {}
        self.znach = {}
        
    def process_input(self, input_text):
        """
        ???????????? ????????? ?????
        """
        words_split = input_text.split()
        
        # ??????? ???? ?? ?????? ??????????
        for j in range(len(words_split)):
            if words_split[j] and words_split[j][-1] in [':', ';', ',', '.', '!', '?']:
                words_split[j] = words_split[j][:-1]
        
        return words_split
    
    def stem_words(self, words_split):
        """
        ????????? ???????? ????
        """
        self.groups.clear()
        
        for word in words_split:
            stem = self.stemmer.stem(word)
            self.groups[stem].append(word)
        
        # ?????????? ? JSON
        self.output_data.clear()
        for stem, word_list in self.groups.items():
            self.output_data[stem] = sorted(word_list)
        
        return self.output_data
    
    def compare_with_chastii(self):
        """
        ?????????? ?????? ? chastii.itog
        """
        if not hasattr(chastii, 'itog'):
            return False, "chastii.itog ?? ??????"
        
        self.znach.clear()
        k = 0
        
        for i in range(len(chastii.itog)):
            current_item = chastii.itog[i]
            
            if isinstance(current_item, dict):
                for j in self.output_data:
                    if j in current_item:
                        if k in self.znach:
                            self.znach[k] += len(current_item[j])
                        else:
                            self.znach[k] = len(current_item[j])
            k += 1
        
        return True, "OK"
    
    def find_max_values(self):
        """
        ??????? ????? ? ????????????? ??????????
        """
        if not self.znach:
            return [], 0
        
        max_value = max(self.znach.values())
        max_keys = [key for key, value in self.znach.items() if value == max_value]
        
        return max_keys, max_value
    
    def get_paragraphs(self, numbers):
        """
        ???????? ?????? ?? ???????
        """
        if not hasattr(chastii, 'dffbdfmvo'):
            return []
        
        paragraphs = []
        for num in numbers:
            index = num - 1
            if 0 <= index < len(chastii.dffbdfmvo):
                paragraph = chastii.dffbdfmvo[index]
                paragraphs.append({
                    'number': num,
                    'content': paragraph
                })
        
        return paragraphs
    
    def run(self, question):
        """
        ???????? ????? ??????? ?????????
        """
        try:
            # ????????? ?????
            words = self.process_input(question)
            
            # ????????
            self.stem_words(words)
            
            # ????????? ? chastii
            success, message = self.compare_with_chastii()
            if not success:
                return {
                    'success': False,
                    'error': message
                }
            
            # ????? ???????????? ????????
            max_keys, max_value = self.find_max_values()
            
            # ????????? ???????
            paragraphs = self.get_paragraphs([key + 1 for key in max_keys])
            
            return {
                'success': True,
                'max_value': max_value,
                'max_keys': max_keys,
                'paragraphs': paragraphs,
                'words': words,
                'stemmed_words': dict(self.output_data),
                'matches': self.znach
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# ??????? ????????? ??????????
processor = QuestionProcessor()

@app.route('/api/process', methods=['POST'])
def process_question():
    """
    API endpoint ??? ????????? ???????
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'success': False,
                'error': '?????? ?? ????? ???? ??????'
            }), 400
        
        result = processor.run(question)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    ???????? ????????????????? API
    """
    return jsonify({
        'status': 'OK',
        'message': 'API is running'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)