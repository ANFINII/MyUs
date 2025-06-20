import { UserMe } from 'types/internal/auth'
import Avatar from 'components/parts/Avatar'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import style from './Comment.module.scss'

interface Props {
  user: UserMe
  count: number
  value?: string
  onChange?: (value: string) => void
  onClick?: () => void
}

export default function CommentInput(props: Props): JSX.Element {
  const { user, count, value, onChange, onClick } = props

  return (
    <form method="POST" action="">
      <Vertical gap="4">
        <p>コメント総数<span className="ml_4">{count}</span></p>
        <Horizontal gap="4">
          <Avatar src={user.avatar} title={user.nickname} size="40" color="grey" className={style.avatar} />
          {user.isActive ? (
            <TextareaLine name="text" placeholder="コメント入力" onChange={onChange} className={style.textarea} />
          ) : (
            <TextareaLine name="text" placeholder="コメントするにはログインが必要です!" disabled className={style.textarea} />
          )}
        </Horizontal>
        <Horizontal align="end">
          <Button color="blue" size="s" name="コメント" disabled={!value?.trim()} onClick={onClick} />
        </Horizontal>
      </Vertical>
    </form>
  )
}
