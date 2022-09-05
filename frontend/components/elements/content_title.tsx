export default function ContentTitle() {
  return (
    <>
      <span className="view_good">
        <div className="view_good_font content_nickname">
          {/* {{ item.author.nickname }} */}
        </div>

        <div className="view_good_font view_good_inline">
          <i title="閲覧数" className="bi bi-caret-right-square view_good_space"></i>
          {/* {{ item.read|intcomma }} */}
        </div>

        <div className="view_good_font view_good_inline">
          <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
          {/* {{ item.total_like|intcomma }} */}
        </div>

        <div className="view_good_font">
          {/* <time>{{ item.created|naturaltime }}</time> */}
        </div>
      </span>
    </>
  )
}
