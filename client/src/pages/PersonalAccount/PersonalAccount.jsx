import { useUser } from '@entities'
import { useAchievements } from '@entities/achievement/model/useAchievements'
import { useMyQuizzes } from '@entities/myQuizzes/model/useMyQuizzes'
import { useQuizHistory } from '@entities/quizHistory/model/useQuizHistory'
import { useProfileStats } from '@entities/user/model/useProfileStats'
import { ProfileStats, QuizHistory } from '@widgets'

import styles from './PersonalAccount.module.scss'

export function PersonalAccount({
  onBackToHome,
  onCreateQuiz,
  onOpenSettings,
}) {
  const storeUser = useUser()
  const { stats } = useProfileStats()

  const userData = {
    name: storeUser?.name || storeUser?.nickname || '',
    email: storeUser?.email || '',
    avatar: storeUser?.avatar || null,
    level: storeUser?.level || 1,
    totalQuizzes: stats.totalQuizzes,
    averageScore: stats.averageScore,
    bestScore: stats.bestResult,
    totalTime: stats.totalMinutes,
  }

  const { history } = useQuizHistory()
  const { myQuizzes, deleteQuiz } = useMyQuizzes()
  const { achievements } = useAchievements()

  return (
    <div className={styles.profilePage}>
      <div className={styles.container}>
        <ProfileStats
          onBackToHome={onBackToHome}
          onOpenSettings={onOpenSettings}
          user={userData}
        />
        <QuizHistory
          onCreateQuiz={onCreateQuiz}
          recentQuizzes={history}
          myQuizzes={myQuizzes}
          achievements={achievements}
          onDeleteQuiz={deleteQuiz}
        />
      </div>
    </div>
  )
}
