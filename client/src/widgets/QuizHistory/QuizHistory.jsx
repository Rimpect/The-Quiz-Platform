import { useState } from 'react'

import styles from './QuizHistory.module.scss'
import { AchievementsTab, HistoryTab, MyQuizzesTab } from './Tabs'

export function QuizHistory({
  onCreateQuiz,
  recentQuizzes = [],
  myQuizzes = [],
  achievements = [],
  onDeleteQuiz,
}) {
  const [historyPage, setHistoryPage] = useState(1)
  const [myQuizzesPage, setMyQuizzesPage] = useState(1)
  const [activeTab, setActiveTab] = useState('history')
  const ITEMS_PER_PAGE = 5

  // Пагинация для истории
  const historyTotalPages = Math.ceil(recentQuizzes.length / ITEMS_PER_PAGE)
  const historyStartIndex = (historyPage - 1) * ITEMS_PER_PAGE
  const paginatedHistory = recentQuizzes.slice(
    historyStartIndex,
    historyStartIndex + ITEMS_PER_PAGE,
  )

  // Пагинация для моих квизов
  const myQuizzesTotalPages = Math.ceil(myQuizzes.length / ITEMS_PER_PAGE)
  const myQuizzesStartIndex = (myQuizzesPage - 1) * ITEMS_PER_PAGE
  const paginatedMyQuizzes = myQuizzes.slice(
    myQuizzesStartIndex,
    myQuizzesStartIndex + ITEMS_PER_PAGE,
  )

  return (
    <div className={styles.historyCard}>
      <div className={styles.tabs}>
        <div className={styles.tabsList}>
          <button
            className={`${styles.tabTrigger} ${activeTab === 'history' ? styles.active : ''}`}
            onClick={() => setActiveTab('history')}
          >
            История
          </button>
          <button
            className={`${styles.tabTrigger} ${activeTab === 'my-quizzes' ? styles.active : ''}`}
            onClick={() => setActiveTab('my-quizzes')}
          >
            Мои квизы
          </button>
          <button
            className={`${styles.tabTrigger} ${activeTab === 'achievements' ? styles.active : ''}`}
            onClick={() => setActiveTab('achievements')}
          >
            Достижения
          </button>
        </div>

        {activeTab === 'history' && (
          <HistoryTab
            recentQuizzes={paginatedHistory}
            currentPage={historyPage}
            totalPages={historyTotalPages}
            onPageChange={setHistoryPage}
          />
        )}

        {activeTab === 'my-quizzes' && (
          <MyQuizzesTab
            onCreateQuiz={onCreateQuiz}
            myQuizzes={paginatedMyQuizzes}
            currentPage={myQuizzesPage}
            totalPages={myQuizzesTotalPages}
            onPageChange={setMyQuizzesPage}
            onDelete={onDeleteQuiz}
          />
        )}

        {activeTab === 'achievements' && (
          <AchievementsTab achievements={achievements} />
        )}
      </div>
    </div>
  )
}
