from datetime import datetime

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status

from ..crud import crud_quiz
from ..schemas.schemas_quiz import QuizCreate, QuizUpdate, QuizBulkCreate
from ..models.model_user import UserRole


class QuizService :
    """Сервис для работы с квизами"""

    def __init__(self, db: Session) :
        self.db = db

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    def get_quiz(self, quiz_id: int) -> Optional[Dict] :
        """Получение квиза с преобразованием в dict"""
        quiz = crud_quiz.get_quiz(self.db, quiz_id)
        if not quiz :
            return None
        return self._quiz_to_dict(quiz)

    def get_quiz_with_details(self, quiz_id: int) -> Optional[Dict] :
        """Получение полного квиза с вопросами и ответами"""
        quiz = crud_quiz.get_quiz_with_details(self.db, quiz_id)
        if not quiz :
            return None
        return self._quiz_full_to_dict(quiz)

    def get_quizzes_list(
            self,
            is_guest: bool = False,
            category_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict] :
        """Получение списка квизов с учётом прав гостя"""
        quizzes = crud_quiz.get_quizzes(
            self.db,
            skip=skip,
            limit=limit,
            category_id=category_id,
            is_public=True
        )

        # Фильтрация для гостей
        if is_guest :
            quizzes = [q for q in quizzes if q.quiz_mode == "single"]

        return [self._quiz_to_dict(q) for q in quizzes]

    def get_quiz_for_edit(self, quiz_id: int, user_id: int, user_role: str) -> Optional[Dict] :
        """Получение квиза для редактирования (с проверкой прав)"""
        quiz = crud_quiz.get_quiz_with_details(self.db, quiz_id)
        if not quiz :
            return None

        # Проверка прав
        if quiz.author_id != user_id and user_role != UserRole.ADMIN :
            return None

        return self._quiz_edit_to_dict(quiz)

    def get_quiz_leaderboard(self, quiz_id: int, limit: int = 100) -> List[Dict] :
        """Получение таблицы лидеров"""
        from ..crud import crud_quiz_result

        # Проверяем существование квиза
        if not crud_quiz.get_quiz(self.db, quiz_id) :
            return []

        return crud_quiz.get_quiz_leaderboard(self.db, quiz_id, limit)

    # ========== СОЗДАНИЕ КВИЗОВ ==========

    def create_quiz(self, quiz_data: QuizCreate, user_id: int, user_role: str) -> Dict :
        """Создание квиза (админ — сразу публикуется)"""
        is_admin = user_role == UserRole.ADMIN
        status = "approved" if is_admin else "pending"

        quiz_dict = {
            "title" : quiz_data.title,
            "category_id" : quiz_data.category_id,
            "description" : quiz_data.description,
            "cover_url" : quiz_data.cover_url,
            "is_public" : is_admin,
            "quiz_mode" : quiz_data.quiz_mode,
            "difficulty" : quiz_data.difficulty,
            "status" : status,
            "author_id" : user_id,
            "lobby_wait_time_seconds" : getattr(quiz_data, "lobby_wait_time_seconds", 30),
            "max_team_members" : getattr(quiz_data, "max_team_members", 10),
        }

        quiz = crud_quiz.create_quiz_record(self.db, quiz_dict)

        return {
            "id" : quiz.id,
            "title" : quiz.title,
            "status" : status,
            "message" : "Quiz created successfully"
        }

    def create_quiz_bulk(self, quiz_data: QuizBulkCreate, user_id: int, user_role: str) -> Dict :
        """Массовое создание квиза с вопросами и ответами"""
        is_admin = user_role == UserRole.ADMIN
        status = "approved" if is_admin else "pending"

        # 1. Создаём квиз
        quiz_dict = {
            "title" : quiz_data.title,
            "category_id" : quiz_data.category_id,
            "description" : quiz_data.description,
            "cover_url" : quiz_data.cover_url,
            "is_public" : is_admin,
            "quiz_mode" : quiz_data.quiz_mode,
            "difficulty" : getattr(quiz_data, "difficulty", "easy"),
            "status" : status,
            "author_id" : user_id,
            "lobby_wait_time_seconds" : getattr(quiz_data, "lobby_wait_time_seconds", 30),
            "max_team_members" : getattr(quiz_data, "max_team_members", 10),
        }

        quiz = crud_quiz.create_quiz_record(self.db, quiz_dict)

        questions_created = 0
        answers_created = 0
        total_seconds = 0

        # 2. Создаём вопросы и ответы
        for q_data in quiz_data.questions :
            question_dict = {
                "quiz_id" : quiz.id,
                "answer_type" : q_data.answer_type,
                "points" : q_data.points,
                "question_text" : q_data.question_text,
                "question_media_url" : getattr(q_data, "media_url", None),
                "time_limit_seconds" : q_data.time_limit_seconds,
            }
            question = crud_quiz.create_question_record(self.db, question_dict)
            questions_created += 1
            total_seconds += q_data.time_limit_seconds or 0

            for idx, a_data in enumerate(q_data.answers) :
                answer_dict = {
                    "question_id" : question.id,
                    "answer_text" : a_data.answer_text,
                    "is_correct" : a_data.is_correct,
                    "order_number" : a_data.order_number or idx,
                }
                crud_quiz.create_answer_record(self.db, answer_dict)
                answers_created += 1

        self.db.commit()

        return {
            "quiz_id" : quiz.id,
            "title" : quiz.title,
            "status" : status,
            "questions_created" : questions_created,
            "answers_created" : answers_created,
            "total_time_limit_minutes" : total_seconds // 60,
        }

    # ========== ОБНОВЛЕНИЕ КВИЗОВ ==========

    def update_quiz(self, quiz_id: int, quiz_update: QuizUpdate, user_id: int, user_role: str) -> Optional[Dict] :
        """Обновление квиза (только автор или админ)"""
        author_id = crud_quiz.get_quiz_author_id(self.db, quiz_id)
        if not author_id :
            return None

        if author_id != user_id and user_role != UserRole.ADMIN :
            return None

        update_data = quiz_update.model_dump(exclude_unset=True)
        if not update_data :
            return None

        quiz = crud_quiz.update_quiz_record(self.db, quiz_id, update_data)
        return self._quiz_to_dict(quiz) if quiz else None

    def update_quiz_bulk(
            self,
            quiz_id: int,
            quiz_data: QuizBulkCreate,
            user_id: int,
            user_role: str
    ) -> Optional[Dict] :
        """Полное обновление квиза с вопросами"""
        author_id = crud_quiz.get_quiz_author_id(self.db, quiz_id)
        if not author_id :
            return None

        is_admin = user_role == UserRole.ADMIN
        if author_id != user_id and not is_admin :
            return None

        new_status = "approved" if is_admin else "pending"

        # 1. Обновляем квиз
        update_data = {
            "title" : quiz_data.title,
            "description" : quiz_data.description,
            "category_id" : quiz_data.category_id,
            "quiz_mode" : quiz_data.quiz_mode,
            "difficulty" : getattr(quiz_data, "difficulty", "easy"),
            "status" : new_status,
            "is_public" : is_admin,
            "lobby_wait_time_seconds" : getattr(quiz_data, "lobby_wait_time_seconds", 30),
            "max_team_members" : getattr(quiz_data, "max_team_members", 10),
            "updated_at" : datetime.utcnow()
        }

        crud_quiz.update_quiz_record(self.db, quiz_id, update_data)

        # 2. Удаляем старые вопросы и ответы
        crud_quiz.delete_questions_by_quiz(self.db, quiz_id)

        questions_created = 0
        answers_created = 0
        total_seconds = 0

        # 3. Создаём новые вопросы и ответы
        for q_data in quiz_data.questions :
            question_dict = {
                "quiz_id" : quiz_id,
                "answer_type" : q_data.answer_type,
                "points" : q_data.points,
                "question_text" : q_data.question_text,
                "question_media_url" : getattr(q_data, "media_url", None),
                "time_limit_seconds" : q_data.time_limit_seconds,
            }
            question = crud_quiz.create_question_record(self.db, question_dict)
            questions_created += 1
            total_seconds += q_data.time_limit_seconds or 0

            for idx, a_data in enumerate(q_data.answers) :
                answer_dict = {
                    "question_id" : question.id,
                    "answer_text" : a_data.answer_text,
                    "is_correct" : a_data.is_correct,
                    "order_number" : a_data.order_number or idx,
                }
                crud_quiz.create_answer_record(self.db, answer_dict)
                answers_created += 1

        self.db.commit()

        return {
            "quiz_id" : quiz_id,
            "title" : quiz_data.title,
            "status" : new_status,
            "questions_created" : questions_created,
            "answers_created" : answers_created,
            "total_time_limit_minutes" : total_seconds // 60,
        }

    # ========== УДАЛЕНИЕ КВИЗОВ ==========

    def delete_quiz(self, quiz_id: int, user_id: int, user_role: str) -> bool :
        """Удаление квиза (автор или админ)"""
        author_id = crud_quiz.get_quiz_author_id(self.db, quiz_id)
        if not author_id :
            return False

        is_admin = user_role == UserRole.ADMIN
        if author_id != user_id and not is_admin :
            return False

        return crud_quiz.delete_quiz_record(self.db, quiz_id)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def can_guest_access(self, quiz_id: int) -> bool :
        """Проверка доступа для гостя"""
        quiz = crud_quiz.get_quiz(self.db, quiz_id)
        if not quiz :
            return False
        return quiz.is_public and quiz.quiz_mode == "single"

    def check_quiz_exists(self, quiz_id: int) -> bool :
        """Проверка существования квиза"""
        return crud_quiz.get_quiz(self.db, quiz_id) is not None

    def get_user_quizzes(self, user_id: int) -> Dict[str, List[Dict]]:
        """Получение всех квизов пользователя по статусу"""
        user_quizzes = crud_quiz.get_user_quizzes(self.db, user_id)
        return {
            "approved": [self._quiz_to_dict(q) for q in user_quizzes["approved"]],
            "pending": [self._quiz_to_dict(q) for q in user_quizzes["pending"]],
            "rejected": [self._quiz_to_dict(q) for q in user_quizzes["rejected"]],
        }

    def get_quiz_categories(self) -> List[str]:
        """Получение всех категорий квизов"""
        return crud_quiz.get_quiz_categories(self.db)

    def can_edit_quiz(self, quiz_id: int, user_id: int, user_role: str) -> bool:
        """Проверка прав на редактирование квиза"""
        author_id = crud_quiz.get_quiz_author_id(self.db, quiz_id)
        if not author_id:
            return False
        return author_id == user_id or user_role == UserRole.ADMIN

    def can_delete_quiz(self, quiz_id: int, user_id: int, user_role: str) -> bool:
        """Проверка прав на удаление квиза"""
        return self.can_edit_quiz(quiz_id, user_id, user_role)

    # ========== ПРЕОБРАЗОВАНИЯ ==========

    def _quiz_to_dict(self, quiz) -> Dict :
        """Преобразование Quiz в dict для ответа"""
        return {
            "id" : quiz.id,
            "title" : quiz.title,
            "category_id" : quiz.category_id,
            "category" : quiz.category_ref.category_type if quiz.category_ref else None,
            "description" : quiz.description,
            "cover_url" : quiz.cover_url,
            "is_public" : quiz.is_public,
            "quiz_mode" : quiz.quiz_mode,
            "difficulty" : getattr(quiz, "difficulty", "easy"),
            "status" : getattr(quiz, "status", "approved"),
            "author_id" : quiz.author_id,
            "created_at" : quiz.created_at.isoformat() if quiz.created_at else None,
            "updated_at" : quiz.updated_at.isoformat() if quiz.updated_at else None,
            "total_questions" : len(quiz.questions) if quiz.questions else 0,
        }

    def _quiz_full_to_dict(self, quiz) -> Dict :
        """Преобразование полного квиза в dict"""
        result = self._quiz_to_dict(quiz)
        result["questions"] = []

        for question in quiz.questions :
            q_dict = {
                "id" : question.id,
                "answer_type" : question.answer_type,
                "points" : question.points,
                "question_text" : question.question_text,
                "media_url" : getattr(question, "question_media_url", None),
                "time_limit_seconds" : question.time_limit_seconds,
                "answers" : []
            }

            for answer in question.answers :
                q_dict["answers"].append({
                    "id" : answer.id,
                    "answer_text" : answer.answer_text,
                    "is_correct" : answer.is_correct,
                    "order_number" : answer.order_number,
                })

            result["questions"].append(q_dict)

        return result

    def _quiz_edit_to_dict(self, quiz) -> Dict :
        """Преобразование квиза для редактора"""
        return {
            "id" : quiz.id,
            "title" : quiz.title,
            "description" : quiz.description or "",
            "categoryId" : str(quiz.category_id) if quiz.category_id else "",
            "difficulty" : getattr(quiz, "difficulty", "easy"),
            "quizMode" : quiz.quiz_mode or "single",
            "lobbyWaitTimeSeconds" : getattr(quiz, "lobby_wait_time_seconds", 30),
            "maxTeamMembers" : getattr(quiz, "max_team_members", 10),
            "coverUrl" : quiz.cover_url or "",
            "status" : getattr(quiz, "status", "approved"),
            "questions" : [
                {
                    "id" : q.id,
                    "questionText" : q.question_text,
                    "questionType" : getattr(q.answer_type, "value", q.answer_type) or "single",
                    "timeLimitSeconds" : q.time_limit_seconds or 0,
                    "points" : q.points or 10,
                    "mediaUrl" : getattr(q, "question_media_url", ""),
                    "answers" : [
                        {
                            "id" : a.id,
                            "text" : a.answer_text,
                            "isCorrect" : a.is_correct,
                        }
                        for a in sorted(q.answers, key=lambda x : x.order_number)
                    ],
                }
                for q in quiz.questions
            ],
        }