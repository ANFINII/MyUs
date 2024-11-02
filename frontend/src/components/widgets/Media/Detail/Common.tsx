import { useState } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { Author, MediaUser } from 'types/internal/media'
import { formatDatetime } from 'utils/functions/datetime'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import CountRead from 'components/parts/Count/Read'
import ExImage from 'components/parts/ExImage'

interface Props {
  title: string
  content: string
  read: number
  totalLike?: number
  commentCount?: number
  created: string
  author: Author
  user?: MediaUser
}

export default function MediaDetailCommon(props: Props) {
  const { title, content, read, totalLike, commentCount, created, author, user } = props
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
    <div className="article_detail_section_1">
      <div className="article_detail_aria">
        <h1 title={title}>{title}</h1>

        <time className="article_detail_aria_1">{formatDatetime(created)}</time>

        <div className="article_detail_aria_2">
          <CountRead read={read} />
          <CountLike isLike={isLike} disable={Boolean(!user)} totalLike={totalLike} onClick={handleLike} />
        </div>

        <div className="article_detail_aria_3">{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </div>

      <hr />

      <label className="content_detail_label" onClick={handleContentView}>
        {isContentView ? '拡大表示' : '縮小表示'}
      </label>

      <div className={clsx('content_detail_aria', isContentView ? 'active' : '')}>
        <div className="content_detail">
          {/* <a href="{% url 'myus:userpage' object.author.nickname %}" data="{{ object.author.nickname }}" className="pjax_button_userpage"> */}
          <Link href="">
            <ExImage src={author.avatar} title={author.nickname} className="profile_image_detail" />
          </Link>
          <div className="username_space">{author.nickname}</div>
          <div className="registered_person">
            登録者数
            <span className="follower_count">{author.followerCount}</span>
          </div>
          <p className="content_detail_p1">{content}</p>
          <div className="content_detail_p2">
            {user?.nickname == author.nickname || (!user && <Button color="green" name="フォローする" disabled />)}
            {user && (
              <form method="POST" action="" className="follow_form">
                {user.isFollow ? <Button color="red" name="解除する" className="follow_change" /> : <Button color="green" name="フォローする" className="follow_change" />}
              </form>
            )}
          </div>
        </div>
      </div>

      <hr />

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

      <hr className="comment_aria_hr" />

      <div className="advertise_aria">
        <h2>広告表示</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article_auto.html' %} */}</article>
        <hr />

        <h2>個別広告</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article.html' %} */}</article>
      </div>
    </div>
  )
}
