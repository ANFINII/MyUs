import { NextRouter, useRouter } from 'next/router'

interface OutProps {
  router: NextRouter
  handleRouter: (url: string) => Promise<boolean>
}

export default function useRouters(): OutProps {
  const router = useRouter()

  const handleRouter = async (url: string) => {
    await router.prefetch(url)
    return router.push(url)
  }

  return { router, handleRouter }
}
