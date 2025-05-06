import { useState } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { Comment } from 'types/internal/comment'
import { Author, CommnetIn, MediaUser } from 'types/internal/media'
import { createComment } from 'api/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AuthorLink from 'components/parts/AuthorLink'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import CountRead from 'components/parts/Count/Read'
import Divide from 'components/parts/Divide'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import Zoom from 'components/widgets/ Zoom'
import CommentInput from 'components/widgets/Comment/Input'

interface Props {
  media: {
    title: string
    content: string
    read: number
    like?: number
    created: Date
    comments: Comment[]
    author: Author
    user?: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): JSX.Element {
  const { media, handleToast } = props
  const { title, content, read, like, created, comments, author, user, type } = media

  const router = useRouter()
  const [isLike, setIsLike] = useState<boolean>(Boolean(user?.isLike))
  const [isContentView, setIsContentVIew] = useState<boolean>(false)
  const [isCommentView, setIsCommentView] = useState<boolean>(false)
  const [text, setText] = useState<string>('')

  const handleComment = (value: string): void => setText(value)
  const handleContentView = () => setIsContentVIew(!isContentView)
  const handleCommentView = () => setIsCommentView(!isCommentView)

  const handleLike = () => {
    setIsLike(!isLike)
  }

  const handleMediaComment = async () => {
    const id = Number(router.query.id)
    const request: CommnetIn = { text, type }
    try {
      await createComment(id, request)
      setText('')
    } catch {
      handleToast('エラーが発生しました！', true)
    }
  }

  return (
    <div>
      <div className="media_detail_aria">
        <h1 title={title}>{title}</h1>

        <time className="media_detail_aria_1">{formatDatetime(created)}</time>

        <div className="media_detail_aria_2">
          <CountRead read={read} />
          <CountLike isLike={isLike} disable={Boolean(!user)} like={like} onClick={handleLike} />
        </div>

        <div className="media_detail_aria_3">{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </div>

      <Divide />

      <div className="content_detail">
        <Horizontal gap="4" align="between">
          <Horizontal gap="4">
            <AuthorLink src={author.avatar} size="3em" imgSize="48" nickname={author.nickname} />
            <Vertical gap="2">
              <p className="fs_14">{author.nickname}</p>
              <p className="fs_14 text_sub">
                登録者数<span className="ml_8">{author.followerCount}</span>
              </p>
            </Vertical>
          </Horizontal>
          <div className="content_detail_p2">
            {user?.nickname === author.nickname || (!user && <Button color="green" name="フォローする" disabled />)}
            {user && (
              <form method="POST" action="" className="follow_form">
                {user.isFollow ? <Button color="red" name="解除する" className="follow_change" /> : <Button color="green" name="フォローする" className="follow_change" />}
              </form>
            )}
          </div>
        </Horizontal>
        <div className="content_detail_p1">
          <Vertical gap="2">
            <Zoom isView={isContentView} onView={handleContentView} />
            <div className={clsx('content_detail_aria', isContentView ? 'active' : '')}>
              <p>{content}</p>
            </div>
          </Vertical>
        </div>
      </div>

      <Divide />

      <CommentInput user={user} count={comments.length} value={text} onChange={handleComment} onClick={handleMediaComment} />
      <Zoom isView={isCommentView} onView={handleCommentView} />
      <div id="comment_aria" className="comment_aria">
        {/* {% include 'parts/common/comment/comment.html' %} */}
      </div>

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
