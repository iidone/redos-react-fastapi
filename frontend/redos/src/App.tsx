import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/AdminDashboard';
import OrganizerDashboard from './pages/OrganizerDashboard';
import MemberDashboard from './pages/MemberDashboard';
import NotFound from './pages/NotFound';

function App() {

  const { user } = useContext(AuthContext)
  const isAuthenticated = !!user;
  const userRole = user?.role || 'guest'

  return (
    <Routes>
      <Route 
        path="/" 
        element={isAuthenticated ? <Navigate to={`/${userRole}`} /> : <Navigate to="/login" />} 
      />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      {isAuthenticated && (
        <>
          <Route path="/admin" element={userRole === 'admin' ? <AdminDashboard /> : <Navigate to="/" />} />
          <Route path="/organizer" element={userRole === 'organizer' ? <OrganizerDashboard /> : <Navigate to="/" />} />
          <Route path="/member" element={userRole === 'member' ? <MemberDashboard /> : <Navigate to="/" />} />
        </>
      )}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;