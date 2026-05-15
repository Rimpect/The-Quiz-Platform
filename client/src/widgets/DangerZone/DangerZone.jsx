import { Button } from '@shared'

import styles from './DangerZone.module.scss'

export function DangerZone() {
  const handleDelete = () => {
    // TODO: delete account

    alert('Аккаунт удален')
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Опасная зона</h2>

      <p className={styles.text}>
        После удаления аккаунта все данные будут потеряны.
      </p>
      <Button variant="red" fullWidth onClick={handleDelete}>
        Удалить аккаунт
      </Button>
    </div>
  )
}
