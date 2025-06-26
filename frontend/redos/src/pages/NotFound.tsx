import '../css/NotFound.css';    


const NotFound = () => {
    return (
    <>
    <header className="dashboard-header" style={{ backgroundColor: 'rgb(51 51 51)' }}>
      <div className="central-header-content">
        <img src="src/assets/logo.png" alt="" className="logo"/>
        <h1 className="header-title">RED OS</h1>
      </div>
    </header>  
    <form>
      <div className='notfound'>
        <h1>
          404 
        </h1>
        <p>
          &nbsp;
        </p>
        <p>
           Not Found
        </p>
      </div>
    </form>
    </>
  );
}
export default NotFound;