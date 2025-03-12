import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { ChatIn } from 'types/internal/media'
import { postChatCreate } from 'api/internal/media/create'
import { nowDate } from 'utils/functions/datetime'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import Vertical from 'components/parts/Stack/Vertical'

export default function ChatCreate(): JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<ChatIn>({ title: '', content: '', period: '' })

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })

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
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Chat" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="">
          <Vertical gap="8">
            <Input label="タイトル" name='title' required={isRequired} onChange={handleInput} />
            <Textarea label="内容" name='content' required={isRequired} onChange={handleText} />
            <Input label="期間" name='period' placeholder={`${nowDate.year}-12-31`} required={isRequired} onChange={handleInput} />
          </Vertical>
        </form>
      </LoginError>
    </Main>
  )
}
