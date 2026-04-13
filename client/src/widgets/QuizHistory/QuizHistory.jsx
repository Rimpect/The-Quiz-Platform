import { useState } from "react";
import {
  FileText,
  Plus,
  Edit,
  Trash2,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import styles from "./QuizHistory.module.scss";

export function QuizHistory({
  onCreateQuiz,
  recentQuizzes = [],
  myQuizzes = [],
  achievements = [],
}) {
  const [historyPage, setHistoryPage] = useState(1);
  const [myQuizzesPage, setMyQuizzesPage] = useState(1);
  const [activeTab, setActiveTab] = useState("history");
  const ITEMS_PER_PAGE = 5;

  const historyTotalPages = Math.ceil(recentQuizzes.length / ITEMS_PER_PAGE);
  const historyStartIndex = (historyPage - 1) * ITEMS_PER_PAGE;
  const paginatedHistory = recentQuizzes.slice(
    historyStartIndex,
    historyStartIndex + ITEMS_PER_PAGE,
  );

  const myQuizzesTotalPages = Math.ceil(myQuizzes.length / ITEMS_PER_PAGE);
  const myQuizzesStartIndex = (myQuizzesPage - 1) * ITEMS_PER_PAGE;
  const paginatedMyQuizzes = myQuizzes.slice(
    myQuizzesStartIndex,
    myQuizzesStartIndex + ITEMS_PER_PAGE,
  );

  const getStatusBadge = (status) => {
    const variants = {
      approved: { label: "Одобрен", className: styles.badgeApproved },
      pending: { label: "На модерации", className: styles.badgePending },
      rejected: { label: "Отклонен", className: styles.badgeRejected },
    };
    const variant = variants[status];
    return (
      <span className={`${styles.badge} ${variant.className}`}>
        {variant.label}
      </span>
    );
  };

  const getScoreColor = (score) => {
    if (score >= 90) return styles.scoreHigh;
    if (score >= 70) return styles.scoreMedium;
    if (score >= 50) return styles.scoreLow;
    return styles.scoreVeryLow;
  };

  return (
    <div className={styles.historyCard}>
      <div className={styles.tabs}>
        <div className={styles.tabsList}>
          <button
            className={`${styles.tabTrigger} ${activeTab === "history" ? styles.active : ""}`}
            onClick={() => setActiveTab("history")}
          >
            История
          </button>
          <button
            className={`${styles.tabTrigger} ${activeTab === "my-quizzes" ? styles.active : ""}`}
            onClick={() => setActiveTab("my-quizzes")}
          >
            Мои квизы
          </button>
          <button
            className={`${styles.tabTrigger} ${activeTab === "achievements" ? styles.active : ""}`}
            onClick={() => setActiveTab("achievements")}
          >
            Достижения
          </button>
        </div>

        {activeTab === "history" && (
          <div className={styles.tabContent}>
            <div className={styles.tabHeader}>
              <h2 className={styles.tabTitle}>
                История квизов ({recentQuizzes.length})
              </h2>
            </div>
            <div className={styles.quizzesList}>
              {paginatedHistory.map((quiz) => (
                <div key={quiz.id} className={styles.quizItem}>
                  <div className={styles.quizContent}>
                    <div className={styles.quizInfo}>
                      <h3 className={styles.quizTitle}>{quiz.title}</h3>
                      <p className={styles.quizCategory}>{quiz.category}</p>
                      <div className={styles.quizMeta}>
                        <span>
                          {quiz.correctAnswers}/{quiz.totalQuestions} правильных
                        </span>
                        <span>•</span>
                        <span>{quiz.time}</span>
                        <span>•</span>
                        <span>{quiz.date}</span>
                      </div>
                    </div>
                    <div
                      className={`${styles.quizScore} ${getScoreColor(quiz.score)}`}
                    >
                      {quiz.score}%
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {historyTotalPages > 1 && (
              <div className={styles.pagination}>
                <p className={styles.paginationInfo}>
                  Показано {historyStartIndex + 1}-
                  {Math.min(
                    historyStartIndex + ITEMS_PER_PAGE,
                    recentQuizzes.length,
                  )}{" "}
                  из {recentQuizzes.length}
                </p>
                <div className={styles.paginationButtons}>
                  <button
                    className={styles.paginationBtn}
                    onClick={() => setHistoryPage(historyPage - 1)}
                    disabled={historyPage === 1}
                  >
                    <ChevronLeft size={16} />
                    Назад
                  </button>
                  <div className={styles.paginationPage}>
                    <span>
                      Страница {historyPage} из {historyTotalPages}
                    </span>
                  </div>
                  <button
                    className={styles.paginationBtn}
                    onClick={() => setHistoryPage(historyPage + 1)}
                    disabled={historyPage === historyTotalPages}
                  >
                    Вперед
                    <ChevronRight size={16} />
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "my-quizzes" && (
          <div className={styles.tabContent}>
            <div className={styles.tabHeader}>
              <h2 className={styles.tabTitle}>
                Созданные квизы ({myQuizzes.length})
              </h2>
              <button onClick={onCreateQuiz} className={styles.createBtn}>
                <Plus size={16} />
                Создать квиз
              </button>
            </div>
            {myQuizzes.length === 0 ? (
              <div className={styles.emptyState}>
                <FileText className={styles.emptyIcon} />
                <p className={styles.emptyText}>
                  У вас пока нет созданных квизов
                </p>
                <button onClick={onCreateQuiz} className={styles.createBtn}>
                  <Plus size={16} />
                  Создать первый квиз
                </button>
              </div>
            ) : (
              <>
                <div className={styles.quizzesList}>
                  {paginatedMyQuizzes.map((quiz) => (
                    <div key={quiz.id} className={styles.quizItem}>
                      <div className={styles.quizContent}>
                        <div className={styles.quizInfo}>
                          <div className={styles.quizHeader}>
                            <h3 className={styles.quizTitle}>{quiz.title}</h3>
                            {getStatusBadge(quiz.status)}
                          </div>
                          <p className={styles.quizCategory}>{quiz.category}</p>
                          <div className={styles.quizMeta}>
                            <span>Участников: {quiz.participants}</span>
                            {quiz.status === "approved" && (
                              <>
                                <span>•</span>
                                <span>Рейтинг: {quiz.rating}</span>
                              </>
                            )}
                            <span>•</span>
                            <span>{quiz.createdAt}</span>
                          </div>
                        </div>
                        <div className={styles.quizActions}>
                          <button className={styles.iconBtn}>
                            <Edit size={16} />
                          </button>
                          <button
                            className={`${styles.iconBtn} ${styles.deleteBtn}`}
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </div>
                      {quiz.status === "rejected" && (
                        <div className={styles.rejectionMessage}>
                          Причина отклонения: Недостаточно уникальных вопросов
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {myQuizzesTotalPages > 1 && (
                  <div className={styles.pagination}>
                    <p className={styles.paginationInfo}>
                      Показано {myQuizzesStartIndex + 1}-
                      {Math.min(
                        myQuizzesStartIndex + ITEMS_PER_PAGE,
                        myQuizzes.length,
                      )}{" "}
                      из {myQuizzes.length}
                    </p>
                    <div className={styles.paginationButtons}>
                      <button
                        className={styles.paginationBtn}
                        onClick={() => setMyQuizzesPage(myQuizzesPage - 1)}
                        disabled={myQuizzesPage === 1}
                      >
                        <ChevronLeft size={16} />
                        Назад
                      </button>
                      <div className={styles.paginationPage}>
                        <span>
                          Страница {myQuizzesPage} из {myQuizzesTotalPages}
                        </span>
                      </div>
                      <button
                        className={styles.paginationBtn}
                        onClick={() => setMyQuizzesPage(myQuizzesPage + 1)}
                        disabled={myQuizzesPage === myQuizzesTotalPages}
                      >
                        Вперед
                        <ChevronRight size={16} />
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {activeTab === "achievements" && (
          <div className={styles.tabContent}>
            <div className={styles.tabHeader}>
              <h2 className={styles.tabTitle}>
                Достижения ({achievements.filter((a) => a.unlocked).length}/
                {achievements.length})
              </h2>
            </div>
            <div className={styles.achievementsGrid}>
              {achievements.map((achievement, index) => (
                <div
                  key={index}
                  className={`${styles.achievementCard} ${
                    achievement.unlocked ? styles.unlocked : styles.locked
                  }`}
                >
                  <div className={styles.achievementIcon}>
                    {achievement.icon}
                  </div>
                  <h3 className={styles.achievementTitle}>
                    {achievement.title}
                  </h3>
                  <p className={styles.achievementDescription}>
                    {achievement.description}
                  </p>
                  {achievement.unlocked && (
                    <div className={styles.achievementUnlocked}>✓ Получено</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
