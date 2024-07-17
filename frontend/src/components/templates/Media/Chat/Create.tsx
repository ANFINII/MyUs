import { useState } from 'react'
import { useRouter } from 'next/router'
import { postChatCreate } from 'api/media/post'
import { ChatIn } from 'types/internal/media'
import { nowDate } from 'utils/functions/datetime'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

export default function ChatCreate() {
  const { year } = nowDate()
  const router = useRouter()
  const { user } = useUser()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<ChatIn>({ title: '', content: '', period: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handlePeriod = (period: string) => setValues({ ...values, period })

  const handleForm = async () => {
    const { title, content, period } = values
    if (!(title && content && period)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postChatCreate(values)
      router.push(`/media/chat/${data.id}`)
    } catch (e) {
      console.log(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Chat">
      <LoginRequired isAuth={user.isActive}>
        <form method="POST" action="" encType="multipart/form-data">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <Input label="期間" className="mt_16" placeholder={`${year}-12-31`} required={isRequired} onChange={handlePeriod} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
