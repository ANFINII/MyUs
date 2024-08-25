import { useState } from 'react'
import router from 'next/router'
import { postTodoCreate } from 'api/internal/media/create'
import { TodoIn } from 'types/internal/media'
import { priority, progress } from 'utils/constants/todo'
import { nowDate } from 'utils/functions/datetime'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

export default function TodoCreate() {
  const { user } = useUser()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<TodoIn>({ title: '', content: '', priority: priority[0].value, progress: progress[0].value, duedate: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handlePriority = (priority: string) => setValues({ ...values, priority })
  const handleProgress = (progress: string) => setValues({ ...values, progress })
  const handleDuedate = (duedate: string) => setValues({ ...values, duedate })

  const handleForm = async () => {
    const { title, content, duedate } = values
    if (!(title && content && duedate)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postTodoCreate(values)
      router.push(`/media/todo/${data.id}`)
    } catch (e) {
      console.log(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Todo" type="table" buttonArea={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginRequired isAuth={user.isActive} margin="mt_20">
        <form method="POST" action="" className="create_grid">
          <Input label="タイトル" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" required={isRequired} onChange={handleContent} />

          <Select label="優先度" options={priority} value={values.priority} onChange={handlePriority} />

          <Select label="進捗度" options={progress} value={values.progress} onChange={handleProgress} />

          <Input label="期日" placeholder={`${nowDate.year}-12-31`} required={isRequired} onChange={handleDuedate} />
        </form>
      </LoginRequired>
    </Main>
  )
}
