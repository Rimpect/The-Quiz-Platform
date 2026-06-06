import styles from '../Quiz.module.scss'

export const AntiCheatWarning = ({ violationsCount }) => {
  if (violationsCount === 0) return null

  const getWarningClass = () => {
    if (violationsCount === 1) return styles.warningOne
    if (violationsCount === 2) return styles.warningTwo
    return styles.warningThree
  }

  return (
    <div className={`${styles.antiCheatWarning} ${getWarningClass()}`}>
      <span>⚠️</span>
      <div className={styles.warningContent}>
        <strong>Предупреждение {violationsCount}/3</strong>
        <p>Не нарушайте правила! При 3 нарушениях квиз будет заблокирован.</p>
      </div>
    </div>
  )
}
