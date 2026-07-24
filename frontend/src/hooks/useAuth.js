import { useSelector, useDispatch } from 'react-redux'
import { login, register, logout, clearError } from '../features/auth/authSlice'

export function useAuth() {
  const dispatch = useDispatch()
  const { user, isAuthenticated, loading, error } = useSelector((state) => state.auth)

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login: (credentials) => dispatch(login(credentials)),
    register: (data) => dispatch(register(data)),
    logout: () => dispatch(logout()),
    clearError: () => dispatch(clearError()),
  }
}
