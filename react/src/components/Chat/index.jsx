import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import { logout } from '../../api/auth';
import './styles.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetchMessages();
  }, [navigate]);

  const fetchMessages = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const data = await getMessages(token);
      setMessages(data);
    } catch (err) {
      setError('Ошибка загрузки сообщений');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!messageText.trim()) {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      setSending(true);
      setError('');
      await sendMessage(messageText, token);
      setMessageText('');
      await fetchMessages();
    } catch (err) {
      setError('Ошибка отправки сообщения');
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await logout(token);
      } catch (err) {
        console.error(err);
      }
    }
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="chat-container" data-easytag="id3-react/src/components/Chat/index.jsx">
      <div className="chat-header">
        <h1>Групповой чат</h1>
        <div className="chat-header-actions">
          <Link to="/profile" className="profile-link">Профиль</Link>
          <button onClick={handleLogout} className="logout-button">Выйти</button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="messages-container">
        {loading ? (
          <div className="loading">Загрузка сообщений...</div>
        ) : messages.length === 0 ? (
          <div className="no-messages">Нет сообщений. Начните беседу!</div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div key={message.id} className="message-item">
                <div className="message-author">{message.author}</div>
                <div className="message-text">{message.text}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={messageText}
          onChange={(e) => setMessageText(e.target.value)}
          placeholder="Введите сообщение..."
          className="message-input"
          disabled={sending}
          maxLength={5000}
        />
        <button type="submit" className="send-button" disabled={sending || !messageText.trim()}>
          {sending ? 'Отправка...' : 'Отправить'}
        </button>
      </form>
    </div>
  );
};

export default Chat;
