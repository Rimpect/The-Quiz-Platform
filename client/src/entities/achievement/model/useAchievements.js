import { useEffect, useState } from 'react'

import { ACHIEVEMENTS_LIST } from '../achievementsList'
import { getMyAchievements } from '../api/achievementApi'

export function useAchievements() {
  const [achievements, setAchievements] = useState(
    ACHIEVEMENTS_LIST.map((a) => ({ ...a, unlocked: false })),
  )
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let canceled = false

    const fetch = async () => {
      setLoading(true)
      try {
        const data = await getMyAchievements()
        if (canceled) return
        const statusMap = data?.achievements || {}
        setAchievements(
          ACHIEVEMENTS_LIST.map((a) => ({
            ...a,
            unlocked: statusMap[String(a.id)] === true,
          })),
        )
      } catch {
        if (!canceled) setError('Не удалось загрузить достижения')
      } finally {
        if (!canceled) setLoading(false)
      }
    }

    fetch()
    return () => {
      canceled = true
    }
  }, [])

  return { achievements, loading, error }
}
