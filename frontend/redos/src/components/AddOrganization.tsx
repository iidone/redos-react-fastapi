import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import 'bulma/css/bulma.min.css';
import '../css/AddMember.css';

const AddOrganization = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
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

    if (!formData.name) {
      setError('Organization name is required');
      setLoading(false);
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      
      await axios.post(
        'http://127.0.0.1:8000/v1/organizations/organizations',
        {
          name: formData.name,
          description: formData.description,
          created_by: currentUser.user_id
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      navigate('/adminorganizations');
    } catch (err) {
      console.error('Error adding organization:', err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || 'Failed to add organization. Please try again.');
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
              onClick={() => navigate('/adminorganizations')}
            >
              Back to Organizations
            </button>
          </div>
        </div>
      </header>
      
      <div className="dashboard-container" style={{ justifyContent: 'center', maxWidth: '45vw'}}>
        <div className="table-container-add" style={{ maxWidth: '45vw' }}>
          <div className="table-header">
            <h2 className="table-title">Create organization</h2>
          </div>
          
          <form onSubmit={handleSubmit}>
            <table className="data-table">
              <tbody>
                <tr>
                  <td style={{ width: '30%' }}>Name</td>
                  <td>
                    <input
                      className="input"
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      placeholder="Organization name"
                    />
                  </td>
                </tr>
                <tr>
                  <td>Description</td>
                  <td>
                    <textarea
                      className="input"
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      placeholder="Organization description"
                      style={{ minHeight: '100px' }}
                      maxLength={200}
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
                Create Organization
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default AddOrganization;