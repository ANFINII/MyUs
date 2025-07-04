import { useState } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { Comment } from 'types/internal/comment'
import { Author, FollowIn, CommnetIn, MediaUser } from 'types/internal/media'
import { postFollow, postComment } from 'api/internal/media/detail'
import { FetchError } from 'utils/constants/enum'
import { isActive } from 'utils/functions/common'
import { formatDatetime } from 'utils/functions/datetime'
import { useUser } from 'components/hooks/useUser'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import CountRead from 'components/parts/Count/Read'
import Divide from 'components/parts/Divide'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import CommentInput from 'components/widgets/Comment/Input/Input'
import Zoom from 'components/widgets/Zoom'
import CommentArea from './CommentArea'

interface Props {
  media: {
    title: string
    content: string
    read: number
    like?: number
    created: Date
    comments: Comment[]
    author: Author
    mediaUser: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): JSX.Element {
  const { media, handleToast } = props
  const { title, content, read, like, created, comments, author, mediaUser, type } = media

  const router = useRouter()
  const { user } = useUser()
  const [isLike, setIsLike] = useState<boolean>(mediaUser.isLike)
  const [isFollow, setIsFollow] = useState<boolean>(mediaUser.isFollow)
  const [isContentView, setIsContentView] = useState<boolean>(false)
  const [isCommentView, setIsCommentView] = useState<boolean>(false)
  const [text, setText] = useState<string>('')

  const isFallowDisable = !user || user.nickname === author.nickname
  const handleLike = () => setIsLike(!isLike)
  const handleContentView = () => setIsContentView(!isContentView)
  const handleCommentView = () => setIsCommentView(!isCommentView)
  const handleComment = (e: React.ChangeEvent<HTMLTextAreaElement>): void => setText(e.target.value)

  const handleFollow = async () => {
    const request: FollowIn = { nickname: author.nickname }
    const ret = await postFollow(request)
    if (ret.isErr()) handleToast(FetchError.Post, true)
    handleToast('フォローしました', false)
    setIsFollow(!isLike)
  }

  const handleDeleteFollow = async () => {
    setIsFollow(!isLike)
  }

  const handleMediaComment = async () => {
    const id = Number(router.query.id)
    const request: CommnetIn = { text, type }
    try {
      await postComment(id, request)
      setText('')
    } catch {
      handleToast(FetchError.Post, true)
    }
  }

  return (
    <div>
      <div className="media_detail_aria">
        <h1 title={title}>{title}</h1>

        <time className="media_detail_aria_1">{formatDatetime(created)}</time>

        <div className="media_detail_aria_2">
          <CountRead read={read} />
          <CountLike isLike={isLike} disable={!user.isActive} like={like} onClick={handleLike} />
        </div>

        <div className="media_detail_aria_3">{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </div>

      <Divide />

      <div className="content_detail">
        <HStack gap="4" justify="between">
          <HStack gap="4">
            <AvatarLink src={author.avatar} size="48" nickname={author.nickname} />
            <VStack gap="2">
              <p className="fs_14">{author.nickname}</p>
              <p className="fs_14 text_sub">
                登録者数<span className="ml_8">{author.followerCount}</span>
              </p>
            </VStack>
          </HStack>
          <div className="content_detail_p2">
            {!isFollow && <Button color="green" name="フォローする" disabled={isFallowDisable} onClick={handleFollow} />}
            {isFollow && <Button color="red" name="解除する" onClick={handleDeleteFollow} />}
          </div>
        </HStack>
        <div className="content_detail_p1">
          <VStack gap="2">
            <Zoom isView={isContentView} onView={handleContentView} />
            <div className={clsx('content_detail_aria', isActive(isContentView))}>
              <p>{content}</p>
            </div>
          </VStack>
        </div>
      </div>

      <Divide />

      <CommentInput user={user} count={comments.length} value={text} onChange={handleComment} onClick={handleMediaComment} />
      <VStack gap="6">
        <Zoom isView={isCommentView} onView={handleCommentView} />
        <CommentArea comments={comments} isView={isCommentView} nickname={user.nickname} />
      </VStack>

      <Divide />

      <div className="advertise_aria">
        <h2>広告表示</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article_auto.html' %} */}</article>
        <Divide />

        <h2>個別広告</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article.html' %} */}</article>
      </div>
    </div>
  )
}
