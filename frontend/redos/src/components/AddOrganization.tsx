import { useNavigate } from 'react-router-dom';
import '../css/NotFound.css';    


const AddOrganization = () => {
    const navigate = useNavigate();

    function back() {
        navigate('/admin');
    }

    return (
    <>
    <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
      <div className="central-header-content">
        <img src="src/assets/logo.png" alt="" className="logo"/>
        <h1 className="header-title">Add organization</h1>
        <div className="header-actions">
            <button className="header-button" onClick={back}>Back</button>
          </div>
      </div>
    </header>  
        </>
  );
}
export default AddOrganization;