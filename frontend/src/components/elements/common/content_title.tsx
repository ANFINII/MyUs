interface Props {
  title?: string
  author?: string
  nickname?: string
  read?: string
  totalLike?: string
  created?: string
}

export default function ContentTitle(props: Props) {
  const {title, nickname, read, totalLike, created} = props
  return (
    <>
      <div title={title} className="content_title">{title}</div>

      <span className="view_good">
        <div className="view_good_font content_nickname">
          {nickname}
        </div>

        <div className="view_good_font view_good_inline">
          <i title="閲覧数" className="bi bi-caret-right-square view_good_space"></i>
          {read}
        </div>

        <div className="view_good_font view_good_inline">
          <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
          {totalLike}
        </div>

        <div className="view_good_font">
          <time>{created}</time>
        </div>
      </span>
    </>
  )
}
