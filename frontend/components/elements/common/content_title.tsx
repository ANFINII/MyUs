export default function ContentTitle(datas: any) {
  const data = datas.data
  const author = data.author
  return (
    <>
      <div title={ data.title } className="content_title">{ data.title }</div>

      <span className="view_good">
        <div className="view_good_font content_nickname">
          { author.nickname }
        </div>

        <div className="view_good_font view_good_inline">
          <i title="閲覧数" className="bi bi-caret-right-square view_good_space"></i>
          { data.read }
        </div>

        <div className="view_good_font view_good_inline">
          <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
          { data.total_like }
        </div>

        <div className="view_good_font">
          <time>{ data.created }</time>
        </div>
      </span>
    </>
  )
}
