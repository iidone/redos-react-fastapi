
import 'bulma/css/bulma.min.css';
import '../css/Register.css';

const Register = () => {


  return (
    <>
    <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
      <div className="central-header-content">
        <img src="src/assets/logo.png" alt="" className="logo"/>
        <h1 className="header-title">RED OS</h1>
      </div>
    </header>
    <form className="box">
      <div className="field">
        <label className="label">Username</label>
        <div className="control">
          <input className="input" type="text" placeholder="Ivan2025" required/>
        </div>
      </div>

      <div className="field">
        <label className="label">First name</label>
        <div className="control">
          <input className="input" type="text" placeholder="Ivan" required/>
        </div>
      </div>

      <div className="field">
        <label className="label">Last name</label>
        <div className="control">
          <input className="input" type="text" placeholder="Ivanov" required/>
        </div>
      </div>

      <div className="field">
        <label className="label">Surname</label>
        <div className="control">
          <input className="input" type="text" placeholder="Ivanovich" required/>
        </div>
      </div>

      <div className="field">
        <label className="label">Email</label>
        <div className="control">
          <input className="input" type="email" placeholder="user@example.com" required/>
        </div>
      </div>
    
      <div className="field">
        <label className="label">Password</label>
        <div className="control">
          <input className="input" type="password" placeholder="********" required/>
        </div>
      </div>
      <div className='centrical'>
        <button className="button is-primary" type="submit">Register</button>
      </div>
    </form>
    </>
  );
};

export default Register;