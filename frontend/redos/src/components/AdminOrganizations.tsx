import 'bulma/css/bulma.min.css';
import '../css/AdminDashboard.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface Organization {
  id: number;
  name: string;
  description: string;
  created_by: string;
  created_at: string;
}

const AdminOrganizations = () => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingOrganizations, setLoadingOrganizations] = useState(true);
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredOrganizations = organizations.filter(org => {
    const name = org.name ? org.name.toLowerCase() : '';
    const description = org.description ? org.description.toLowerCase() : '';
    const createdBy = org.created_by ? String(org.created_by).toLowerCase() : '';
    const createdAt = org.created_at ? String(org.created_at).toLowerCase() : '';
    const id = org.id ? String(org.id) : '';
    
    const searchLower = searchTerm.toLowerCase();
    
    return (
      name.includes(searchLower) ||
      description.includes(searchLower) ||
      createdBy.includes(searchLower) ||
      createdAt.includes(searchLower) ||
      id.includes(searchTerm)
    );
  });

  function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  function navigateToAddOrg() {
    navigate('/addorganization');
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/v1/organizations/organizations');
        console.log('Full API Response:', response);

        const orgsData = response.data;
        console.log('Raw organizations data:', orgsData);

        if (!orgsData || !Array.isArray(orgsData)) {
          console.error('Data is not an array:', orgsData);
          return;
        }

        const orgsFromDb = orgsData.map((org: any) => ({
          id: org.id,
          name: org.name || 'No name',
          description: org.description || 'No description',
          created_by: org.created_by || 'Unknown',
          created_at: new Date(org.created_at).toLocaleString() || 'Unkown',
        }));

        console.log('Mapped organizations:', orgsFromDb);
        setOrganizations(orgsFromDb);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoadingOrganizations(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    setLoading(loadingOrganizations);
  }, [loadingOrganizations ]);

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
            <h2 className="table-title">Organizations</h2>
            <div className="table-actions">
              <div className="search-container">
                <input
                  type="text"
                  placeholder="Search organizations..."
                  className="search-input"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <button className="action-button add-button" onClick={navigateToAddOrg}>
                Add organization
              </button>
              <button className="action-button export-button">
                Export to CSV
              </button>
            </div>
            
          </div>
          
          {loadingOrganizations ? (
            <div className="loading-indicator">Loading organizations...</div>
          ) : (
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>№</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Creator</th>
                    <th>Created at</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredOrganizations.map((org, index) => (
                    <tr key={`org-${org.id}`}>
                      <td>{index + 1}</td>
                      <td>{org.name}</td>
                      <td>{org.description}</td>
                      <td>{org.created_by}</td>
                      <td>{org.created_at}</td>
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

export default AdminOrganizations;