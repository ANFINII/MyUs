export default function ContentTitle(author: any) {
  return (
    <>
      <span className="view_good">
        <div className="view_good_font content_nickname">
          { author.nickname }
        </div>

        <div className="view_good_font view_good_inline">
          <i title="閲覧数" className="bi bi-caret-right-square view_good_space"></i>
          { author.read }
        </div>

        <div className="view_good_font view_good_inline">
          <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
          { author.total_like }
        </div>

        <div className="view_good_font">
          <time>{ author.created }</time>
        </div>
      </span>
    </>
  )
}
