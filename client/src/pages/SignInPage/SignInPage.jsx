import { LoginForm } from '@features'
import { IS_DEMO, ROUTES } from '@shared'
import { Navigate } from 'react-router-dom'

export function SignInPage() {
  // В демо-версии авторизация недоступна — пользователь уже «залогинен».
  if (IS_DEMO) return <Navigate to={ROUTES.main} replace />

  return (
    <div>
      <LoginForm></LoginForm>
    </div>
  )
}
