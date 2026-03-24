// QuestionProcessor.jsx
import React, { useState, useEffect } from 'react';
import './QuestionProcessor.css';

const API_URL = 'http://localhost:5000/api';

const QuestionProcessor = () => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Эффект для рисования звезд после загрузки компонента
  useEffect(() => {
    const canvas = document.getElementById("stars");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Устанавливаем размеры canvas
    canvas.width = viewportWidth;
    canvas.height = viewportHeight;
    
    const placeStar = (x, y, size) => {
      ctx.beginPath();
      ctx.arc(x, y, size, 0, 2 * Math.PI);
      ctx.fillStyle = "white";
      ctx.fill();
    };
    
    // Рисуем звезды
    for(let i = 0; i < 100; i++) { // Увеличил количество звезд для лучшего эффекта
      placeStar(
        0.95 * viewportWidth * Math.random(),
        0.95 * viewportHeight * Math.random(),
        2
      );
    }
  }, []); // Пустой массив зависимостей - эффект выполнится только один раз

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Пожалуйста, введите вопрос');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Произошла ошибка при обработке');
      }

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Произошла ошибка при обработке');
      }
    } catch (err) {
      setError(err.message || 'Ошибка подключения к серверу');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderParagraph = (paragraph) => {
    const content = paragraph.content;
    
    if (typeof content === 'object') {
      return (
        <div className="paragraph-object">
          {Object.entries(content).map(([key, value]) => (
            <div key={key} className="paragraph-field">
              <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value}
            </div>
          ))}
        </div>
      );
    }
    
    return <div className="paragraph-text">{content}</div>;
  };

  return (
    <div className="question-processor">
      <canvas id='stars' style={{ 
        position: 'fixed', 
        top: 0, 
        left: 0, 
        width: '100%', 
        height: '100%', 
        zIndex: 0,
        pointerEvents: 'none' 
      }}></canvas>

      <div className='cloudsDiv' style={{ position: 'relative', zIndex: 1 }}>
        <div className='clouds' id="cloud-1"></div>
        <div className='clouds' id="cloud-2"></div>
        <div className='clouds' id="cloud-3"></div>
        <div className='clouds' id="cloud-4"></div>
        <div className='clouds' id="cloud-5"></div>
      </div>
      
      <div style={{ position: 'relative', zIndex: 2 }}>
        <h1>ГХС</h1>
        
        <form onSubmit={handleSubmit} className="question-form">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Введите ваш вопрос..."
            rows="4"
            className="question-input"
          />
          
          <button 
            type="submit" 
            disabled={loading}
            className="submit-button"
          >
            {loading ? 'Обработка...' : 'Отправить вопрос'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <strong>Ошибка:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p id='spinnerText'>Обработка вопроса...</p>
          </div>
        )}

        {result && (
          <div className="results">
            <div className="stats">
              <h2>Результаты обработки</h2>
              <div className="stat-item">
                <strong>Максимальное количество совпадений:</strong> {result.max_value}
              </div>
              <div className="stat-item">
                <strong>Номера абзацев:</strong> {result.max_keys.map(k => k + 1).join(', ')}
              </div>
            </div>
          
            {result.words && result.words.length > 0 && (
              <div className="words-section">
                <h3>Обработанные слова:</h3>
                <div className="word-list">
                  {result.words.map((word, idx) => (
                    <span key={idx} className="word-tag">{word}</span>
                  ))}
                </div>
              </div>
            )}

            {result.stemmed_words && Object.keys(result.stemmed_words).length > 0 && (
              <div className="stemmed-section">
                <h3>Стемминг слов:</h3>
                <div className="stemmed-grid">
                  {Object.entries(result.stemmed_words).map(([stem, words]) => (
                    <div key={stem} className="stemmed-item">
                      <strong>{stem}:</strong> {Array.isArray(words) ? words.join(', ') : words}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.paragraphs && result.paragraphs.length > 0 && (
              <div className="paragraphs-section">
                <h2>Найденные абзацы</h2>
                {result.paragraphs.map((paragraph, idx) => (
                  <div key={idx} className="paragraph-card">
                    <div className="paragraph-header">
                      <h3>Абзац №{paragraph.number}</h3>
                    </div>
                    <div className="paragraph-content">
                      {renderParagraph(paragraph)}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {result.matches && (
              <div className="matches-section">
                <h3>Детальная статистика совпадений:</h3>
                <div className="matches-grid">
                  {Object.entries(result.matches).map(([key, value]) => (
                    <div key={key} className="match-item">
                      <span className="match-key">Абзац {parseInt(key) + 1}:</span>
                      <span className="match-value">{value} совпадений</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

document.body.style.backgroundColor = "#2f184b"

export default QuestionProcessor;