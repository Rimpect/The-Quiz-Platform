import { useIsAuthenticated, useAuthLoading } from '@entities'
import { ROUTES } from '@shared'
import { Navigate } from 'react-router-dom'

export function AppGuard({ children }) {
  const isAuth = useIsAuthenticated()
  const loading = useAuthLoading()

  if (loading) {
    return <div>Loading...</div>
  }

  if (!isAuth) {
    return <Navigate to={ROUTES.auth} replace />
  }

  return children
}
