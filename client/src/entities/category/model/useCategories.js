import { useState, useEffect } from 'react'

import { client } from '@shared/api/client'

export function useCategories() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    client('/categories')
      .then((data) => setCategories(data || []))
      .catch(() => setCategories([]))
      .finally(() => setLoading(false))
  }, [])

  return { categories, loading }
}
