import { useContext } from 'react'

import { AntiCheatContext } from './AntiCheatProvider'

export const useAntiCheatContext = () => {
  const context = useContext(AntiCheatContext)

  if (!context) {
    throw new Error('useAntiCheatContext must be used within AntiCheatProvider')
  }

  return context
}
