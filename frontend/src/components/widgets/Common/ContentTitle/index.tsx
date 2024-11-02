import clsx from 'clsx'
import style from './ContentTitle.module.scss'

interface Props {
  title: string
  nickname: string
  read: number
  totalLike: number
  created: string
}

export default function ContentTitle(props: Props) {
  const { title, nickname, read, totalLike, created } = props

  return (
    <>
      <div title={title} className={style.content_title}>
        {title}
      </div>

      <span className={style.view_good}>
        <div className={clsx(style.view_good_font, style.content_nickname)}>{nickname}</div>

        <div className={clsx(style.view_good_font, style.view_good_inline)}>
          <i title="閲覧数" className="bi bi-caret-right-square mr_2"></i>
          {read}
        </div>

        <div className={clsx(style.view_good_font, style.view_good_inline)}>
          <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
          {totalLike}
        </div>

        <div className={style.view_good_inline}>
          <time>{created}</time>
        </div>
      </span>
    </>
  )
}
