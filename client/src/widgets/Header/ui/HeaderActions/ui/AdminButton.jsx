import React from 'react'

import { Button, ROUTES } from '@shared'
import { Shield } from 'lucide-react'
import { Link } from 'react-router-dom'

export function AdminButton() {
  return (
    <div>
      <Link to={ROUTES.admin}>
        <Button variant="white" size="medium" icon={<Shield size={20} />}>
          Админка
        </Button>
      </Link>
    </div>
  )
}
