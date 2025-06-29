import 'bulma/css/bulma.min.css';
import '../css/AdminDashboard.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number;
  role: string;
  username: string;
  full_name: string;
  email: string;
}

const AdminDashboard = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [tempRole, setTempRole] = useState('');
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  function navigateToAddUser() {
    navigate('/adduser');
  }

  const filteredUsers = users.filter(user => 
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const startEditing = (userId: number, currentRole: string) => {
    setEditingUserId(userId);
    setTempRole(currentRole);
  };

  const cancelEditing = () => {
    setEditingUserId(null);
    setTempRole('');
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setTempRole(e.target.value);
  };

  const saveRole = async (userId: number) => {
    try {
      const token = localStorage.getItem('token');
      
      await axios.patch(
        `http://127.0.0.1:8000/v1/users/${userId}/role`,
        { role: tempRole },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      setUsers(users.map(user => 
        user.id === userId ? { ...user, role: tempRole } : user
      ));
      
      setEditingUserId(null);
    } catch (error) {
      console.error('Error updating role:', error);
      if (axios.isAxiosError(error)) {
        alert(error.response?.data?.detail || 'Failed to update role');
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/v1/users/users');
        console.log('Full API Response:', response);

        const usersData = response.data;
        console.log('Raw users data:', usersData);

        if (!usersData || !Array.isArray(usersData)) {
          console.error('Data is not an array:', usersData);
          return;
        }

        setUsers(usersData.map(user => ({
          id: user.id,
          role: user.role,
          username: user.username,
          full_name: user.full_name,
          email: user.email,
        })));
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoadingUsers(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    setLoading(loadingUsers);
  }, [loadingUsers]);

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
            <button className="header-button" onClick={logout}>Logout</button>
          </div>
        </div>
      </header>
      <div className="dashboard-container">
        <div className="table-container">
          <div className="table-header">
            <h2 className="table-title">Users</h2>
            <div className="table-actions">
              <div className="search-container">
                <input
                  type="text"
                  placeholder="Search users..."
                  className="search-input"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <button className="action-button add-button" onClick={navigateToAddUser}>
                Add user
              </button>
              <button className="action-button export-button">
                Export to CSV
              </button>
            </div>
          </div>
          
          {loadingUsers ? (
            <div className="loading-indicator">Loading users...</div>
          ) : (
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>№</th>
                    <th>Role</th>
                    <th>Actions</th>
                    <th>Username</th>
                    <th>Full name</th>
                    <th>Email</th>
                    
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user, index) => (
                    <tr key={user.id}>
                      <td>{index + 1}</td>
                      <td>
                        {editingUserId === user.id ? (
                          <select
                            className="input"
                            value={tempRole}
                            onChange={handleRoleChange}
                            style={{ width: '100%' }}
                          >
                            <option value="member">Member</option>
                            <option value="organizer">Organizer</option>
                            <option value="admin">Admin</option>
                          </select>
                        ) : (
                          user.role
                        )}
                      </td>
                      <td>
                        {editingUserId === user.id ? (
                          <>
                            <button 
                              className="button is-small is-success mr-2"
                              onClick={() => saveRole(user.id)}
                            >
                              Save
                            </button>
                            <button 
                              className="button is-small is-danger"
                              onClick={cancelEditing}
                            >
                              Cancel
                            </button>
                          </>
                        ) : (
                          <button 
                            className="button is-small"
                            onClick={() => startEditing(user.id, user.role)}
                          >
                            <span className="icon">
                              <i className="fas fa-pencil-alt"></i>
                            </span>
                          </button>
                        )}
                      </td>
                      <td>{user.username}</td>
                      <td>{user.full_name}</td>
                      <td>{user.email}</td>
                      
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default AdminDashboard;