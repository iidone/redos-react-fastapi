import 'bulma/css/bulma.min.css';
import '../css/AdminDashboard.css';
import { useEffect, useState } from 'react';
import axios from 'axios';

interface Member {
  id: number;
  member_id: number;
  organization_id: number;
  organizer_id: number;
  assigned_at: string;
}

interface Organization {
  id: number;
  name: string;
  description: string;
  created_by: string;
  created_at: string;
}

const MembersTable = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingOrganizations, setLoadingOrganizations] = useState(true);
  const [loadingMembers, setLoadingMembers] = useState(true);

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
        created_at: org.created_at || new Date().toISOString(),
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
  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/v1/organizations_members/organizations_members');
      console.log('Full API Response:', response);

      const membersData = response.data;
      console.log('Raw members data:', membersData);

      if (!membersData || !Array.isArray(membersData)) {
        console.error('Data is not an array:', membersData);
        return;
      }

      setMembers(membersData.map(member => ({
        id: Number(member.member_id) * 100000 + Number(member.organization_id),
        member_id: member.member_id,
        organization_id: member.organization_id,
        organizer_id: member.organizer_id,
        assigned_at: new Date(member.assigned_at).toLocaleString()
      })));
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoadingMembers(false);
    }
  };

  fetchData();
}, []);

useEffect(() => {
  setLoading(loadingOrganizations || loadingMembers);
}, [loadingOrganizations, loadingMembers]);

  return (
    <>
    <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
      <div className="header-content">
        <img src="src/assets/logo.png" alt="" className="logo"/>
        <h1 className="header-title">Admin Dashboard</h1>
        <div className="header-actions">
          <button className="header-button">Logout</button>
        </div>
      </div>
    </header>
    <div className="dashboard-container">
      <div className="table-container">
        <div className="table-header">
          <h2 className="table-title">Members</h2>
          <div className="table-actions">
            <button className="action-button add-button">
              Add member
            </button>
            <button className="action-button export-button">
              Export to CSV
            </button>
          </div>
        </div>
        
        {loadingMembers ? (
          <div className="loading-indicator">Loading members...</div>
        ) : (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>№</th>
                  <th>Member</th>
                  <th>Organization</th>
                  <th>Assigned by</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {members.map((member, index) => (
                  <tr key={`${member.member_id}-${member.organization_id}`}>
                    <td>{index + 1}</td>
                    <td>{member.member_id}</td>
                    <td>{member.organization_id}</td>
                    <td>{member.organizer_id}</td>
                    <td>{member.assigned_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="table-container">
        <div className="table-header">
          <h2 className="table-title">Organizations</h2>
          <div className="table-actions">
            <button className="action-button add-button">
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
                {organizations.map((org, index) => (
                  <tr key={org.id}>
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

export default MembersTable;