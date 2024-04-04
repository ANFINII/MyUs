import { useState } from 'react'
import { useRouter } from 'next/router'
import { postChatCreate } from 'api/media/post'
import { ChatIn } from 'types/internal/media'
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
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<ChatIn>({ title: '', content: '', period: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handlePeriod = (period: string) => setData({ ...data, period })

  const handleForm = async () => {
    if (!(data.title && data.content && data.period)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
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
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <Input label="期間" className="mt_16" placeholder={`${year}-12-31`} required={isRequired} onChange={handlePeriod} />

          <Button color="green" name="作成する" loading={isLoading} onClick={handleForm} className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
