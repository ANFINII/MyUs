import { MediaUser } from 'types/internal/media'
import { isEmpty } from 'utils/constants/common'
import Button from 'components/parts/Button'
import Image from 'components/parts/Image'
import TextareaLine from 'components/parts/Input/Textarea/Line'

interface Props {
  user: MediaUser
  commentCount: number
}

export default function CommentInput(props: Props) {
  const { user, commentCount } = props

  return (
    <form method="POST" action="" id="comment_form" obj-id="{{ obj_id }}">
      <div className="comment_input">
        <p>
          コメント総数
          <span id="comment_count">{commentCount}</span>
        </p>
        {!isEmpty(user) ? (
          <>
            <Image src="/image/user_icon.png" alt="" title="Anonymous" className="profile_image_comment" />
            <TextareaLine name="text" placeholder="コメントするにはログインが必要です!" disabled></TextareaLine>
            <Button blue disabled size="xs" name="コメント" type="submit" className="button" />
          </>
        ) : (
          <>
            <Image src="{user.image}" alt="" title={user?.nickname} className="profile_image_comment" />
            <TextareaLine name="text" placeholder="コメント入力" id="comment_area" className="textarea_br"></TextareaLine>
            <Button blue disabled={false} size="xs" name="コメント" type="submit" className="button" />
          </>
        )}
      </div>
    </form>
  )
}
