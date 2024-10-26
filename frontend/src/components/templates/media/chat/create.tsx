import { useState } from 'react'
import { useRouter } from 'next/router'
import { postChatCreate } from 'api/internal/media/create'
import { ChatIn } from 'types/internal/media'
import { nowDate } from 'utils/functions/datetime'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'
import Vertical from 'components/parts/Stack/Vertical'

export default function ChatCreate() {
  const router = useRouter()
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
    <Main title="Chat" type="table" buttonArea={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginRequired margin="mt_20">
        <form method="POST" action="">
          <Vertical gap="8">
            <Input label="タイトル" required={isRequired} onChange={handleTitle} />
            <Textarea label="内容" required={isRequired} onChange={handleContent} />
            <Input label="期間" placeholder={`${nowDate.year}-12-31`} required={isRequired} onChange={handlePeriod} />
          </Vertical>
        </form>
      </LoginRequired>
    </Main>
  )
}
