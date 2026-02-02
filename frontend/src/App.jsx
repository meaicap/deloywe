import { useState, useEffect } from 'react'
import Login from './components/Login'
import { Layout } from './components/Layout' // To be created
import axios from 'axios';

function App() {
  const [user, setUser] = useState(null);

  // Check valid session on mount? 
  // For now, simpler to just require login every refresh or rely on localStorage if we implemented persistence.
  // The backend uses stateless auth or simple verification? 
  // app.py stores user in st.session_state only.
  // We can persist user in localStorage.

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Layout user={user} onLogout={handleLogout} />
  )
}

export default App
