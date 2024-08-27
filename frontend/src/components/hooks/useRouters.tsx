import { useEffect, useState } from 'react'
import { NextRouter, useRouter } from 'next/router'

interface OutProps {
  router: NextRouter
  handleRouter: (url: string) => Promise<boolean>
  location?: Location
}

export default function useRouters(): OutProps {
  const router = useRouter()
  const [location, setLocation] = useState<Location>()
  useEffect(() => setLocation(window.location), [])

  const handleRouter = (url: string) => router.push(url)
  return { router, handleRouter, location }
}
