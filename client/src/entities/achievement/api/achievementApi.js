import { client } from '@shared/api/client'

export const getMyAchievements = () => client('/achievements')
