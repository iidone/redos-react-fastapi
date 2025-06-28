import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import 'bulma/css/bulma.min.css';
import '../css/AdminDashboard.css';

interface Organization {
  id: number;
  name: string;
}

interface User {
  id: number;
  full_name: string;
  username: string;
  role: string;
}

const AddMember = () => {
  const [formData, setFormData] = useState({
    member_id: '',
    member_name: '',
    organization_id: '',
    organization_name: ''
  });
  
  const [allOrganizations, setAllOrganizations] = useState<Organization[]>([]);
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [filteredOrganizations, setFilteredOrganizations] = useState<Organization[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [showOrgDropdown, setShowOrgDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [orgsResponse, usersResponse] = await Promise.all([
          axios.get('http://127.0.0.1:8000/v1/organizations/organizations'),
          axios.get('http://127.0.0.1:8000/v1/users/users', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
        ]);
        
        setAllOrganizations(orgsResponse.data);
        setAllUsers(usersResponse.data.filter((user: User) => user.role === 'member'));
      } catch (err) {
        console.error('Error fetching data:', err);
      }
    };
    
    fetchData();
  }, []);

  const handleOrgSearch = (searchTerm: string) => {
    setFormData(prev => ({
      ...prev,
      organization_name: searchTerm,
      organization_id: searchTerm === '' ? '' : prev.organization_id
    }));

    if (searchTerm.length > 0) {
      const filtered = allOrganizations.filter(org =>
        org.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredOrganizations(filtered);
      setShowOrgDropdown(true);
    } else {
      setShowOrgDropdown(false);
    }
  };

  const handleUserSearch = (searchTerm: string) => {
    setFormData(prev => ({
      ...prev,
      member_name: searchTerm,
      member_id: searchTerm === '' ? '' : prev.member_id
    }));

    if (searchTerm.length > 0) {
      const filtered = allUsers.filter(user =>
        user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.username.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredUsers(filtered);
      setShowUserDropdown(true);
    } else {
      setShowUserDropdown(false);
    }
  };

  const selectOrganization = (org: Organization) => {
    setFormData(prev => ({
      ...prev,
      organization_id: org.id.toString(),
      organization_name: org.name
    }));
    setShowOrgDropdown(false);
  };

  const selectUser = (user: User) => {
    setFormData(prev => ({
      ...prev,
      member_id: user.id.toString(),
      member_name: user.full_name
    }));
    setShowUserDropdown(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!formData.member_id || !formData.organization_id) {
      setError('Please select both member and organization');
      setLoading(false);
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      
      const response = await axios.post(
        'http://127.0.0.1:8000/v1/organizations_members/',
        {
          member_id: Number(formData.member_id),
          organization_id: Number(formData.organization_id),
          organizer_id: currentUser.user_id
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
      console.error('Error adding member:', err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || 'Failed to add member. Please try again.');
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
          <img src="src/assets/logo.png" alt="" className="logo"/>
          <h1 className="header-title">Admin Dashboard</h1>
          <div className="header-actions">
            <button 
              className="header-button" 
              onClick={() => navigate('/admin')}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>
      
      <div className="dashboard-container" style={{ justifyContent: 'center' }}>
        <div className="table-container" style={{ maxWidth: '800px' }}>
          <div className="table-header">
            <h2 className="table-title">Add Member to Organization</h2>
          </div>
          
          <form onSubmit={handleSubmit}>
            <table className="data-table">
              <tbody>
                <tr>
                  <td style={{ width: '30%' }}>Member</td>
                  <td style={{ position: 'relative' }}>
                    <input
                      className="input"
                      type="text"
                      name="member_name"
                      value={formData.member_name}
                      onChange={(e) => {
                        setFormData(prev => ({ ...prev, member_name: e.target.value }));
                        handleUserSearch(e.target.value);
                      }}
                      required
                      placeholder="Search members..."
                    />
                    {showUserDropdown && (
                      <div className="dropdown-list">
                        {filteredUsers.length > 0 ? (
                          filteredUsers.map(user => (
                            <div
                              key={user.id}
                              className="dropdown-item"
                              onClick={() => selectUser(user)}
                            >
                              {user.full_name} ({user.username})
                            </div>
                          ))
                        ) : (
                          <div className="dropdown-item no-results">
                            No members found
                          </div>
                        )}
                      </div>
                    )}
                    <input
                      type="hidden"
                      name="member_id"
                      value={formData.member_id}
                    />
                  </td>
                </tr>
                <tr>
                  <td>Organization</td>
                  <td style={{ position: 'relative' }}>
                    <input
                      className="input"
                      type="text"
                      name="organization_name"
                      value={formData.organization_name}
                      onChange={(e) => {
                        setFormData(prev => ({ ...prev, organization_name: e.target.value }));
                        handleOrgSearch(e.target.value);
                      }}
                      required
                      placeholder="Search organizations..."
                    />
                    {showOrgDropdown && (
                      <div className="dropdown-list">
                        {filteredOrganizations.length > 0 ? (
                          filteredOrganizations.map(org => (
                            <div
                              key={org.id}
                              className="dropdown-item"
                              onClick={() => selectOrganization(org)}
                            >
                              {org.name}
                            </div>
                          ))
                        ) : (
                          <div className="dropdown-item no-results">
                            No organizations found
                          </div>
                        )}
                      </div>
                    )}
                    <input
                      type="hidden"
                      name="organization_id"
                      value={formData.organization_id}
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
                Add to Organization
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default AddMember;