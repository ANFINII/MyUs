import { UserMe } from 'types/internal/auth'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  user: UserMe
  count: number
  loading?: boolean
  value?: string
  onChange?: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  onClick?: () => void
}

export default function CommentInput(props: Props): JSX.Element {
  const { user, count, loading, value, onChange, onClick } = props

  return (
    <form method="POST" action="">
      <VStack gap="4">
        <p>
          コメント総数<span className="ml_4">{count}</span>
        </p>
        <HStack gap="4">
          <AvatarLink src={user.avatar} nickname={user.nickname} />
          {user.isActive ? (
            <TextareaLine name="text" placeholder="コメント入力" value={value} onChange={onChange} />
          ) : (
            <TextareaLine name="text" placeholder="コメントするにはログインが必要です!" disabled />
          )}
        </HStack>
        <HStack justify="end">
          <Button color="blue" size="s" name="コメント" disabled={!value?.trim()} loading={loading} onClick={onClick} />
        </HStack>
      </VStack>
    </form>
  )
}
