import { createContext, useEffect, useState, type ReactNode } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

type User = {
  id: string;
  username: string;
  role: 'admin' | 'organizer' | 'member' | 'guest';
  first_name?: string;
  last_name?: string;
};

type AuthContextType = {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
};

export const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: async () => {},
  logout: () => {},
  error: null,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const login = async (username: string, password: string) => {
  try {
    setError(null);
    
    const response = await axios.post(
      'http://127.0.0.1:8000/v1/users/login',
      new URLSearchParams({
        username: username,
        password: password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    

    const { access_token, user_info } = response.data;

    setToken(access_token);
    const userRole = (user_info?.role?.toLowerCase() || 'guest') as User['role'];
    setUser({
      id: user_info?.user_id?.toString() || '',
      username: user_info?.username || username,
      role: userRole,
      first_name: user_info?.first_name || '',
      last_name: user_info?.last_name || '',
    });

    localStorage.setItem('authToken', access_token);
    localStorage.setItem('user', JSON.stringify(user_info));

    navigate(`/${userRole}`);
  } catch (err) {
    setError('Неверный username или пароль');
    console.error('Login error:', err);
    throw err;
  }
};

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    navigate('/login');
  };

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      try {
        const userInfo = JSON.parse(storedUser);
        setToken(storedToken);
        setUser({
          id: userInfo.user_id.toString(),
          username: userInfo.username,
          role: userInfo.role.toLowerCase() as User['role'],
          first_name: userInfo.first_name,
          last_name: userInfo.last_name,
        });
      } catch (err) {
        console.error('Failed to parse user data', err);
        logout();
      }
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, error }}>
      {children}
    </AuthContext.Provider>
  );
};