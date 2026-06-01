import { useIsAuthenticated, useIsAdmin, useAuthLoading } from '@entities'
import { ROUTES } from '@shared'
import { Navigate } from 'react-router-dom'

export function ProtectedRoute({ children, requireAdmin = false }) {
  const isAuthenticated = useIsAuthenticated()
  const isAdmin = useIsAdmin()
  const loading = useAuthLoading()

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>Загрузка...</div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.notFound} replace />
  }

  if (requireAdmin && !isAdmin) {
    return <Navigate to={ROUTES.notFound} replace />
  }

  return children
}

export function PublicRoute({ children }) {
  const isAuthenticated = useIsAuthenticated()
  const loading = useAuthLoading()

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>Загрузка...</div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to={ROUTES.main} replace />
  }

  return children
}
