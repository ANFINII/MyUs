import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

interface OutProps {
  loading: boolean
  setLoading: React.Dispatch<React.SetStateAction<boolean>>
}

export function useLoading(): OutProps {
  const router = useRouter()
  const [loading, setLoading] = useState<boolean>(false)

  useEffect(() => {
    const startLoading = () => setLoading(true)
    const stopLoading = () => setLoading(false)

    router.events.on('routeChangeStart', startLoading)
    router.events.on('routeChangeComplete', stopLoading)
    router.events.on('routeChangeError', stopLoading)

    return () => {
      router.events.off('routeChangeStart', startLoading)
      router.events.off('routeChangeComplete', stopLoading)
      router.events.off('routeChangeError', stopLoading)
    }
  }, [router])

  return { loading, setLoading }
}
