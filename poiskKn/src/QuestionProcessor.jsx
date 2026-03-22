// QuestionProcessor.jsx - версия с fetch вместо axios
import React, { useState } from 'react';
import './QuestionProcessor.css';

const API_URL = 'http://localhost:5000/api';

const QuestionProcessor = () => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

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
      <h1>Обработчик вопросов</h1>
      
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
          <p>Обработка вопроса...</p>
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
  );
};

export default QuestionProcessor;