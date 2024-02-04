import Link from 'next/link'
import { Blog } from 'types/internal/media'
import { formatDatetime } from 'utils/functions/datetime'
import Button from 'components/parts/Button'
import CommentInput from '../Comment/Input'

interface Props {
  data: Blog
}

export default function MediaDetailCommon(props: Props) {
  const { data } = props
  const { id, title, content, read, totalLike, commentCount, created, author, user } = data
  const { isLike } = user || {}

  const isAuth = false
  const isFollow = true

  return (
    <div className="article_detail_section_1">
      <div className="article_detail_aria">
        <h1 title={title}>{title}</h1>

        <time className="article_detail_aria_1">{formatDatetime(created)}</time>

        <div className="article_detail_aria_2">
          <div className="read">
            <i className="bi bi-caret-right-square icon_font" title="閲覧数"></i>
            <span>{read}</span>
          </div>
          {isAuth ? (
            // <form method="POST" action="" obj-id="{{ object.id }}" path="{{ request.path }}" csrf="{{ csrf_token }}>
            <form method="POST" action="" obj-id={id}>
              {isLike ? (
                <button type="submit" name="like" className="like_form like_fill">
                  <i className="bi bi-hand-thumbs-up-fill icon_font like_color" title="いいね"></i>
                </button>
              ) : (
                <button type="submit" name="like" className="like_form like_no">
                  <i className="bi bi-hand-thumbs-up icon_font like_color" title="いいね"></i>
                </button>
              )}
              <span className="like_count">{totalLike}</span>
            </form>
          ) : (
            <>
              <i className="bi bi-hand-thumbs-up icon_font" title="いいね"></i>
              <span>{totalLike}</span>
            </>
          )}
        </div>

        <div className="article_detail_aria_3">{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </div>
      <hr />

      <input type="checkbox" id="content_detail_check_id" className="content_detail_check" />
      <label htmlFor="content_detail_check_id" className="content_detail_check_label1">
        拡大表示
      </label>
      <label htmlFor="content_detail_check_id" className="content_detail_check_label2">
        縮小表示
      </label>

      <div className="content_detail_aria">
        <div className="content_detail">
          {/* <a href="{% url 'myus:userpage' object.author.nickname %}" data="{{ object.author.nickname }}" className="pjax_button_userpage"> */}
          <Link href="">
            <img src={author.image} title={author.nickname} className="profile_image_detail" />
          </Link>
          <div className="username_space">{author.nickname}</div>
          <div className="registered_person">
            登録者数
            <span className="follower_count">{author.followerCount}</span>
          </div>
          <p className="content_detail_p1">{content}</p>

          <div className="content_detail_p2">
            {user?.nickname == author.nickname || (!isAuth && <Button green disabled name="フォローする" />)}
            {isAuth && (
              <form method="POST" action="" className="follow_form">
                {isFollow ? <Button red name="解除する" className="follow_change" /> : <Button green name="フォローする" className="follow_change" />}
              </form>
            )}
          </div>
        </div>
      </div>
      <hr />

      <CommentInput user={user} commentCount={commentCount} />

      <input type="checkbox" id="comment_aria_check_id" className="comment_aria_check" />
      <label htmlFor="comment_aria_check_id" className="comment_aria_check_label1">
        拡大表示
      </label>
      <label htmlFor="comment_aria_check_id" className="comment_aria_check_label2">
        縮小表示
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
