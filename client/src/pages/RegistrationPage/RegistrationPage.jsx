import { RegistrationForm } from '@features'
import { IS_DEMO, ROUTES } from '@shared'
import { Navigate } from 'react-router-dom'

export function RegistrationPage() {
  // В демо-версии регистрация недоступна — пользователь уже «залогинен».
  if (IS_DEMO) return <Navigate to={ROUTES.main} replace />

  return (
    <div>
      <RegistrationForm></RegistrationForm>
    </div>
  )
}
