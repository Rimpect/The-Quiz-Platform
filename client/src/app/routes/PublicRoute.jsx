import { useIsAuthenticated, useAuthLoading } from '@entities'
import { ROUTES } from '@shared'
import { Navigate } from 'react-router-dom'

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
