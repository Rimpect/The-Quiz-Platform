import { useEffect, useState, useCallback } from 'react'
import { client } from '@shared/api/client'
import { useUser } from '@entities'
import { toast } from 'sonner'

export function useTeamLobby(quizId) {
  const currentUser = useUser()
  const [sessionId, setSessionId] = useState(null)
  const [teams, setTeams] = useState([])
  const [myTeamId, setMyTeamId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)

  // Инициализировать лобби при загрузке
  useEffect(() => {
    if (!quizId) return

    const initializeLobby = async () => {
      try {
        // Создаём session для квиза если её нет
        if (!sessionId && currentUser?.id) {
          const sessionResponse = await client('/game/sessions/create', {
            method: 'POST',
            body: JSON.stringify({
              quiz_id: quizId,
              game_mode: 'team',
              team_id: `temp-${currentUser.id}`,
              team_name: 'Temp',
            }),
          })
          setSessionId(sessionResponse.session_id)
        }
      } catch (err) {
        console.error('Error initializing lobby:', err)
      }
    }

    initializeLobby()

    // Загрузить существующие команды (mock для демо)
    setTeams([
      {
        id: 'team-alpha',
        name: 'Команда Альфа',
        maxMembers: 10,
        members: [
          {
            id: 1,
            name: 'Максим',
            avatar: '',
            isLeader: true,
            isReady: false,
          },
        ],
      },
      {
        id: 'team-beta',
        name: 'Команда Бета',
        maxMembers: 10,
        members: [
          {
            id: 2,
            name: 'Виктор',
            avatar: '',
            isLeader: true,
            isReady: false,
          },
        ],
      },
    ])
  }, [quizId, currentUser, sessionId])

  const createTeam = useCallback(
    async (teamName, description) => {
      if (!quizId || !currentUser?.id) return

      setLoading(true)
      try {
        // Создать игровую сессию с новой командой
        const teamId = `team-${Date.now()}`
        const response = await client('/game/sessions/create', {
          method: 'POST',
          body: JSON.stringify({
            quiz_id: quizId,
            game_mode: 'team',
            team_id: teamId,
            team_name: teamName,
          }),
        })

        setSessionId(response.session_id)
        setMyTeamId(teamId)

        const newTeam = {
          id: teamId,
          name: teamName,
          description,
          maxMembers: 10,
          members: [
            {
              id: currentUser.id,
              name: currentUser.nickname || 'Вы',
              avatar: currentUser.photo_profile || '',
              isLeader: true,
              isReady: false,
            },
          ],
        }

        setTeams([...teams, newTeam])
        toast.success(`Команда "${teamName}" создана`)
        setIsModalOpen(false)

        return { sessionId: response.session_id, teamId }
      } catch (err) {
        toast.error(err.message || 'Ошибка создания команды')
      } finally {
        setLoading(false)
      }
    },
    [quizId, currentUser, teams],
  )

  const joinTeam = useCallback(
    async (teamId) => {
      if (!quizId) {
        toast.error('Квиз не загружен')
        return
      }

      setLoading(true)
      try {
        // Если сессии нет, создаём её перед присоединением к команде
        let currentSessionId = sessionId
        if (!currentSessionId) {
          const sessionResponse = await client('/game/sessions/create', {
            method: 'POST',
            body: JSON.stringify({
              quiz_id: quizId,
              game_mode: 'team',
              team_id: teamId,
              team_name: teams.find(t => t.id === teamId)?.name || 'Team',
            }),
          })
          currentSessionId = sessionResponse.session_id
          setSessionId(currentSessionId)
        }

        // Присоединиться к сессии
        const response = await client('/game/sessions/join', {
          method: 'POST',
          body: JSON.stringify({
            session_id: currentSessionId,
          }),
        })

        // Обновить список команд
        setTeams((prevTeams) =>
          prevTeams.map((team) =>
            team.id === teamId
              ? {
                  ...team,
                  members: [
                    ...team.members,
                    {
                      id: currentUser.id,
                      name: currentUser.nickname || 'Вы',
                      avatar: currentUser.photo_profile || '',
                      isLeader: false,
                      isReady: false,
                    },
                  ],
                }
              : team,
          ),
        )

        setMyTeamId(teamId)
        toast.success('Вы присоединились к команде')
      } catch (err) {
        toast.error(err.message || 'Ошибка присоединения к команде')
      } finally {
        setLoading(false)
      }
    },
    [quizId, sessionId, currentUser],
  )

  const markReady = useCallback(async () => {
    if (!myTeamId) return

    setLoading(true)
    try {
      // Обновить статус "готов"
      setTeams((prevTeams) =>
        prevTeams.map((team) =>
          team.id === myTeamId
            ? {
                ...team,
                members: team.members.map((member) =>
                  member.id === currentUser.id
                    ? { ...member, isReady: true }
                    : member,
                ),
              }
            : team,
        ),
      )

      toast.success('Вы отмечены как готовый')
    } catch (err) {
      toast.error(err.message || 'Ошибка')
    } finally {
      setLoading(false)
    }
  }, [myTeamId, currentUser.id])

  return {
    sessionId,
    teams,
    myTeamId,
    loading,
    isModalOpen,
    setIsModalOpen,
    createTeam,
    joinTeam,
    markReady,
  }
}
