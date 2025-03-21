import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { ApiOut } from 'lib/error'

interface OutProps<T> {
  search?: string
  newDatas: T
}

interface Props<T> {
  datas: T
  getDatas: (search?: string) => Promise<ApiOut<T>>
}

export const useNewDatas = <T extends object>(props: Props<T>): OutProps<T> => {
  const { datas, getDatas } = props

  const router = useRouter()
  const [newDatas, setNewDatas] = useState<T>(datas)

  const search = router.query.search as string
  useEffect(() => {
    const fetchDatas = async (search?: string) => {
      const ret = await getDatas(search)
      if (ret.isErr()) return
      const newDatas = ret.value
      setNewDatas(newDatas)
    }
    fetchDatas(search)
  }, [search])

  return { search, newDatas }
}
