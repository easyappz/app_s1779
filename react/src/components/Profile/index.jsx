import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentMember } from '../../api/members';
import './styles.css';

function Profile() {
  const [member, setMember] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await getCurrentMember(token);
        setMember(data);
        setError(null);
      } catch (err) {
        setError('Не удалось загрузить профиль');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  const handleBackToChat = () => {
    navigate('/chat');
  };

  if (loading) {
    return (
      <div className="profile-container" data-easytag="id4-react/src/components/Profile/index.jsx">
        <div className="profile-loading">Загрузка...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container" data-easytag="id4-react/src/components/Profile/index.jsx">
        <div className="profile-error">{error}</div>
        <button onClick={handleLogout} className="profile-button">Выйти</button>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id4-react/src/components/Profile/index.jsx">
      <div className="profile-card">
        <h1 className="profile-title">Профиль</h1>
        
        {member && (
          <div className="profile-info">
            <div className="profile-field">
              <span className="profile-label">Имя пользователя:</span>
              <span className="profile-value">{member.username}</span>
            </div>
            
            <div className="profile-field">
              <span className="profile-label">Дата регистрации:</span>
              <span className="profile-value">
                {new Date(member.created_at).toLocaleDateString('ru-RU', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
          </div>
        )}
        
        <div className="profile-actions">
          <button onClick={handleBackToChat} className="profile-button profile-button-secondary">
            Вернуться к чату
          </button>
          <button onClick={handleLogout} className="profile-button profile-button-primary">
            Выйти
          </button>
        </div>
      </div>
    </div>
  );
}

export default Profile;
