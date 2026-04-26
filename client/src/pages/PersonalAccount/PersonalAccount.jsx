import {
  mockUser,
  recentQuizzes,
  myQuizzes,
  achievements,
} from '../../MockData'
import { ProfileStats } from '../../widgets/ProfileStats/ProfileStats'
import { QuizHistory } from '../../widgets/QuizHistory/QuizHistory'

import styles from './PersonalAccount.module.scss'

export function PersonalAccount({
  onBackToHome,
  onCreateQuiz,
  onOpenSettings,
  user,
}) {
  const userData = {
    name: user?.name || mockUser.name,
    email: user?.email || mockUser.email,
    avatar: user?.avatar || mockUser.avatar,
    level: user?.level || mockUser.level,
    xp: user?.xp || mockUser.xp,
    nextLevelXp: user?.nextLevelXp || mockUser.nextLevelXp,
    totalQuizzes: user?.totalQuizzes || mockUser.totalQuizzes,
    averageScore: user?.averageScore || mockUser.averageScore,
    bestScore: user?.bestScore || mockUser.bestScore,
    totalTime: user?.totalTime || mockUser.totalTime,
  }

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
          recentQuizzes={recentQuizzes}
          myQuizzes={myQuizzes}
          achievements={achievements}
        />
      </div>
    </div>
  )
}
