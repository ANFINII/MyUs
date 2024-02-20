import { useState } from 'react'
import { useRouter } from 'next/router'
import { postChatCreate } from 'api/media/post'
import { CreateChat } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

const now = new Date()
const year = now.getFullYear()

interface Props {
  isAuth: boolean
}

export default function ChatCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [data, setData] = useState<CreateChat>({ title: '', content: '', period: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handlePeriod = (period: string) => setData({ ...data, period })

  const handleForm = async () => {
    setIsLoading(true)
    console.log('data', data)

    try {
      const chat = await postChatCreate(data)
      router.push(`media/blog/${chat.id}`)
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
          <Textarea name="content" value={data.content} onChange={handleContent} required></Textarea>

          <p className="mv_16">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} onChange={handlePeriod} required />

          <Button green type="button" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
