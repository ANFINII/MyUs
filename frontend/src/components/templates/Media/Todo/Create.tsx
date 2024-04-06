import { useState } from 'react'
import { ToDoIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

const now = new Date()
const year = now.getFullYear()

export const priority = [
  { value: 'danger', label: '高' },
  { value: 'success', label: '普通' },
  { value: 'info', label: '低' },
]

export const progress = [
  { value: '0', label: '未着手' },
  { value: '1', label: '進行中' },
  { value: '2', label: '完了' },
]

interface Props {
  isAuth: boolean
}

export default function TodoCreate(props: Props) {
  const { isAuth } = props

  const [data, setData] = useState<ToDoIn>({ title: '', content: '', priority: '', progress: '' })
  const handlePriority = (priority: string) => setData({ ...data, priority })
  const handleProgress = (progress: string) => setData({ ...data, progress })

  return (
    <Main title="Todo">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="">
          <p className="mv_16">タイトル</p>
          <Input name="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" required />

          <p className="mv_16">優先度</p>
          <Select name="priority" options={priority} value={data.priority} onChange={handlePriority} />

          <p className="mv_16">進捗度</p>
          <Select name="progress" options={progress} value={data.progress} onChange={handleProgress} />

          <p className="mv_16">期日</p>
          <Input name="duedate" placeholder={`${year}-12-31`} required />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
