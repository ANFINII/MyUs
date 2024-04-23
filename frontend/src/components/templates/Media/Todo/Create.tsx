import { useState } from 'react'
import router from 'next/router'
import { postTodoCreate } from 'api/media/post'
import { TodoIn } from 'types/internal/media'
import { priority, progress } from 'utils/constants/todo'
import { nowDate } from 'utils/functions/datetime'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function TodoCreate(props: Props) {
  const { isAuth } = props

  const { year } = nowDate()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<TodoIn>({ title: '', content: '', priority: '', progress: '', duedate: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handlePriority = (priority: string) => setData({ ...data, priority })
  const handleProgress = (progress: string) => setData({ ...data, progress })
  const handleDuedate = (duedate: string) => setData({ ...data, duedate })

  const handleForm = async () => {
    if (!(data.title && data.content && data.duedate)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const chat = await postTodoCreate(data)
      router.push(`/media/todo/${chat.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Todo">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <Select label="優先度" className="mt_16" options={priority} value={data.priority} onChange={handlePriority} />

          <Select label="進捗度" className="mt_16" options={progress} value={data.progress} onChange={handleProgress} />

          <Input label="期日" className="mt_16" placeholder={`${year}-12-31`} required={isRequired} onChange={handleDuedate} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
