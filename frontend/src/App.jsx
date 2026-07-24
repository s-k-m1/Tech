import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import MainLayout from './layouts/MainLayout'
import AuthLayout from './layouts/AuthLayout'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import CrmPage from './pages/crm/CrmPage'
import HrmPage from './pages/hrm/HrmPage'
import ProjectsPage from './pages/projects/ProjectsPage'
import TicketsPage from './pages/tickets/TicketsPage'
import SecurityPage from './pages/security/SecurityPage'

function PrivateRoute({ children }) {
  const { isAuthenticated } = useSelector((state) => state.auth)
  return isAuthenticated ? children : <Navigate to="/auth/login" />
}

export default function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthLayout />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
      </Route>
      <Route
        path="/"
        element={
          <PrivateRoute>
            <MainLayout />
          </PrivateRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="crm/*" element={<CrmPage />} />
        <Route path="hrm/*" element={<HrmPage />} />
        <Route path="projects/*" element={<ProjectsPage />} />
        <Route path="tickets/*" element={<TicketsPage />} />
        <Route path="security/*" element={<SecurityPage />} />
      </Route>
    </Routes>
  )
}
