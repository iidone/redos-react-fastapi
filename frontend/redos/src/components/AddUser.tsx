import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import 'bulma/css/bulma.min.css';
import '../css/AddMember.css';

const AddUser = () => {
  const [formData, setFormData] = useState({
    role: 'member',
    username: '',
    full_name: '',
    password: '',
    email: ''
  });
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!formData.username || !formData.password || !formData.email) {
      setError('Username, password and email are required');
      setLoading(false);
      return;
    }

    try {
      const token = localStorage.getItem('token');
      
      await axios.post(
        'http://127.0.0.1:8000/v1/users/users',
        {
          role: formData.role,
          username: formData.username,
          full_name: formData.full_name,
          password: formData.password,
          email: formData.email
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      navigate('/admin');
    } catch (err) {
      console.error('Error adding user:', err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || 'Failed to add user. Please try again.');
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
        <div className="header-content">
          <div className="centrical-header">
            <img src="src/assets/logo.png" alt="" className="logo"/>
            <button 
              className="header-nav-bar" 
              onClick={() => navigate('/admin')}
            >
              Users
            </button>
            <button 
              className="header-nav-bar" 
              onClick={() => navigate('/adminmembers')}
            >
              Members
            </button>
            <button 
              className="header-nav-bar" 
              onClick={() => navigate('/adminorganizations')}
            >
              Organizations
            </button>
          </div>
          <div className="header-actions">
            <button 
              className="header-button" 
              onClick={() => navigate('/admin')}
            >
              Back to Users
            </button>
          </div>
        </div>
      </header>
      
      <div className="dashboard-container" style={{ justifyContent: 'center', maxWidth: '45vw'}}>
        <div className="table-container-add" style={{ maxWidth: '45vw' }}>
          <div className="table-header">
            <h2 className="table-title">Create user</h2>
          </div>
          
          <form onSubmit={handleSubmit}>
            <table className="data-table">
              <tbody>
                <tr>
                  <td style={{ width: '30%' }}>Role</td>
                  <td>
                    <select
                      className="user-input"
                      name="role"
                      value={formData.role}
                      onChange={handleChange}
                      required
                    >
                      <option value="member">Member</option>
                      <option value="organizer">Organizer</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                </tr>
                <tr>
                  <td>Username</td>
                  <td>
                    <input
                      className="input"
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      placeholder="Username"
                    />
                  </td>
                </tr>
                <tr>
                  <td>Full Name</td>
                  <td>
                    <input
                      className="input"
                      type="text"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      placeholder="Full name"
                    />
                  </td>
                </tr>
                <tr>
                  <td>Email</td>
                  <td>
                    <input
                      className="input"
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      placeholder="Email"
                    />
                  </td>
                </tr>
                <tr>
                  <td>Password</td>
                  <td>
                    <input
                      className="input"
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      placeholder="Password"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
            
            {error && (
              <div className="notification is-danger" style={{ marginTop: '1rem' }}>
                {error}
              </div>
            )}
            
            <div className="table-actions" style={{ justifyContent: 'center', marginTop: '1rem' }}>
              <button 
                type="submit" 
                className={`action-button add-button ${loading ? 'is-loading' : ''}`}
                disabled={loading}
              >
                Create User
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default AddUser;