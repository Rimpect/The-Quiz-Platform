import { useIsAuthenticated, useAuthLoading } from '@entities'
import { Navigate, Outlet } from 'react-router-dom'
import { ROUTES } from '@shared'

export function AppGuard() {
  const isAuth = useIsAuthenticated()
  const loading = useAuthLoading()

  if (loading) return <div>Loading...</div>

  if (!isAuth) {
    return <Navigate to={ROUTES.auth} replace />
  }

  return <Outlet />
}
