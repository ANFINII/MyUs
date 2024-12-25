import { useState } from 'react'
import clsx from 'clsx'
import { Author, MediaUser } from 'types/internal/media'
import { formatDatetime } from 'utils/functions/datetime'
import AuthorLink from 'components/parts/AuthorLink'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import CountRead from 'components/parts/Count/Read'
import Divide from 'components/parts/Divide'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import Zoom from 'components/widgets/ Zoom'

interface Props {
  title: string
  content: string
  read: number
  like?: number
  commentCount?: number
  created: string
  author: Author
  user?: MediaUser
}

export default function MediaDetailCommon(props: Props) {
  const { title, content, read, like, commentCount, created, author, user } = props
  console.log(commentCount)

  const [isLike, setIsLike] = useState<boolean>(Boolean(user?.isLike))
  const [isContentView, setIsContentVIew] = useState<boolean>(false)
  const [isCommentView, setIsCommentView] = useState<boolean>(false)

  const handleContentView = () => setIsContentVIew(!isContentView)
  const handleCommnetView = () => setIsCommentView(!isCommentView)

  const handleLike = () => {
    setIsLike(!isLike)
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
            <AuthorLink src={author.avatar} size='3em' imgSize='48' nickname={author.nickname} />
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

      {/* <CommentInput user={user} commentCount={commentCount} /> */}

      {/* <input type="checkbox" id="comment_aria_check_id" className="comment_aria_check" />
      <label htmlFor="comment_aria_check_id" className="comment_aria_check_label1">
        拡大表示
      </label>
      <label htmlFor="comment_aria_check_id" className="comment_aria_check_label2">
        縮小表示
      </label> */}

      <label className="comment_aria_label" onClick={handleCommnetView}>
        {isCommentView ? '拡大表示' : '縮小表示'}
      </label>

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
