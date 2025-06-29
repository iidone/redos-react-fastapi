import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import 'bulma/css/bulma.min.css';
import '../css/Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login, error: authError } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError('');
    setIsLoading(true);
    
    try {
      await login(username, password);
    } catch (err) {
      setLocalError('Неверный username или пароль');
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
        <div className="central-header-content">
          <img src="src/assets/logo.png" alt="" className="logo"/>
          <h1 className="header-title">RED OS</h1>
        </div>
      </header>
      <div className="login-container">
        <form className="box login" onSubmit={handleSubmit}>
          <div className="field">
            <label className="label">Username</label>
            <div className="control">
              <input 
                className="input" 
                type="text" 
                placeholder="Username" 
                value={username}
                onChange={(e) => setUsername(e.target.value)} 
                required
                autoFocus
              />
            </div>
          </div>
        
          <div className="field">
            <label className="label">Пароль</label>
            <div className="control">
              <input 
                className="input" 
                type="password" 
                placeholder="********" 
                value={password}
                onChange={(e) => setPassword(e.target.value)} 
                required
              />
            </div>
          </div>
          
          {(authError || localError) && (
            <div className="notification-error">
              <button 
                onClick={() => {
                  setLocalError('');
                  if (authError) {
                    useContext(AuthContext).error = null;
                  }
                }}
              />
              {authError || localError}
            </div>
          )}
          
          <div className='centrical'>
            <button 
              className={`button is-primary ${isLoading ? 'is-loading' : ''}`} 
              type="submit"
              disabled={isLoading}
            >
              Войти
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Login;