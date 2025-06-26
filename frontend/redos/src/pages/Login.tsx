import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import 'bulma/css/bulma.min.css';
import '../css/Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
    navigate('/');
  };

  return (
    <>
    <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
      <div className="central-header-content">
        <img src="src/assets/logo.png" alt="" className="logo"/>
        <h1 className="header-title">RED OS</h1>
      </div>
    </header>
    <form className="box login" onSubmit={handleSubmit}>
      <div className="field">
        <label className="label">Email</label>
        <div className="control">
          <input className="input" type="email" placeholder="user@example.com" onChange={(e) => setEmail(e.target.value)} required/>
        </div>
      </div>
    
      <div className="field">
        <label className="label">Password</label>
        <div className="control">
          <input className="input" type="password" placeholder="********" onChange={(e) => setPassword(e.target.value)} required/>
        </div>
      </div>
      <div className='centrical'>
        <button className="button is-primary" type="submit">Login</button>
      </div>
    </form>
    </>
  );
};

export default Login;