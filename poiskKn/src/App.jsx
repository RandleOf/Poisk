import { useState } from 'react'
import './App.css'
import { FaSearch, FaExternalLinkAlt } from 'react-icons/fa';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  
  const searchInNewWindow = () => {
    if (!searchQuery.trim()) {
      alert('Введите поисковый запрос');
      return;
    }
    
    // Поиск в Google
    const googleUrl = `https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`;
    window.open(googleUrl, '_blank', 'width=1200,height=800');
  };
  
  const openSearchSettings = () => {
    window.open('/settings', '_blank', 'width=600,height=400');
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchInNewWindow();
    }
  };
  
  return (
    <div className="search-container">
      <h1>Поисковая система</h1>
      
      <div className="search-box">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Введите запрос..."
          style={{
            padding: '12px',
            width: '400px',
            fontSize: '16px',
            borderRadius: '5px 0 0 5px',
            border: '1px solid #ddd'
          }}
        />
        
        <button
          onClick={searchInNewWindow}
          style={{
            padding: '12px 24px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '0 5px 5px 0',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <FaSearch />
          Искать
        </button>
      </div>
      
      <button
        onClick={openSearchSettings}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px'
        }}
      >
        <FaExternalLinkAlt />
        Расширенный поиск
      </button>
    </div>
  );
}

export default App;