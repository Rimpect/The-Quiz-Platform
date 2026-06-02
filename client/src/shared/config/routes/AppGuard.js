import { useIsAuthenticated, useAuthLoading } from '@entities'
import { ROUTES } from '@shared'
import { Navigate, useLocation } from 'react-router-dom'

export function AppGuard({ children }) {
  const isAuth = useIsAuthenticated()
  const loading = useAuthLoading()
  const location = useLocation()

  if (loading) {
    return <div>Loading...</div>
  }

  if (!isAuth) {
    return <Navigate to={ROUTES.auth} replace state={{ from: location }} />
  }

  return children
}
