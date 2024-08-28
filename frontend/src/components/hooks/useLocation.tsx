import { useState, useEffect } from 'react'

interface OutProps {
  location?: Location
}

export default function useLocation(): OutProps {
  const [location, setLocation] = useState<Location | undefined>(undefined)

  useEffect(() => {
    if (typeof window !== 'undefined') setLocation(window.location)
  }, [])

  return { location }
}
