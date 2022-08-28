export default function SerchTag() {
  return (
    <>
      <nav className="tag_nav">
        <form method="POST" action="" id="tag_form" className="tag_nav_grid">
          <input type="checkbox" id="tag_add" className="tag_menu" />
          <label htmlFor="tag_add" className="main_tag_1"><span className="main_tag_center">タグ</span></label>
          <input type="submit" className="main_tag_2 form_button" value="追加" csrf="{{ csrf_token }}" />
          if (user.is_authenticated) {
            <input type="text" name="searchtag" className="main_tag_3" maxLength="30" placeholder="タグ名" />
          } else {
            <input type="text" name="searchtag" className="main_tag_3" maxLength="30" placeholder="タグ名" disabled />
          }
          <div className="main_tag_n">
            <div className="tag_n_list">
            {/* for (searchtag in searchtag_list) {
              <a href="?search={{ searchtag.name }}" search={{ searchtag.name }} className="pjax_search">{{ searchtag.name }}</a>
            } */}
            </div>
          </div>

          <label htmlFor="tag_add" className="main_tag_4"><span className="main_tag_center">完了</span></label>

          <div className="main_tag_left">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi bi-chevron-left" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
            </svg>
          </div>

          <div className="main_tag_right">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi bi-chevron-right" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
            </svg>
          </div>
        </form>
      </nav>
    </>
  )
}
