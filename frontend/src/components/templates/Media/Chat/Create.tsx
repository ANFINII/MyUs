import { useState } from 'react'
import { useRouter } from 'next/router'
import { postChatCreate } from 'api/media/post'
import { CreateChat } from 'types/internal/media'
import { nowDate } from 'utils/functions/datetime'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function ChatCreate(props: Props) {
  const { isAuth } = props

  const { year } = nowDate()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [data, setData] = useState<CreateChat>({ title: '', content: '', period: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handlePeriod = (period: string) => setData({ ...data, period })

  const handleForm = async () => {
    setIsLoading(true)
    // await new Promise((resolve) => setTimeout(resolve, 3000))
    try {
      const chat = await postChatCreate(data)
      router.push(`/media/chat/${chat.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Chat">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <p className="mv_16">タイトル</p>
          <Input name="title" value={data.title} onChange={handleTitle} required />

          <p className="mv_16">内容</p>
          <Textarea name="content" value={data.content} onChange={handleContent} required />

          <p className="mv_16">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} onChange={handlePeriod} required />

          <Button color="green" name="作成する" loading={isLoading} onClick={handleForm} className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
