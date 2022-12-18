export default function SearchTag() {
  return (
    <nav className="searchtag">
      <form method="POST" action="" id="tag_form" className="searchtag_grid">
        <input type="checkbox" id="searchtag_add" className="searchtag_menu"/>
        <label htmlFor="searchtag_add" className="searchtag_1"><span className="searchtag_center">タグ</span></label>
        <input type="submit" className="searchtag_2 form_button" value="追加" data-csrf="{{ csrf_token }}"/>
        {/* if (user.is_authenticated) { */}
          <input type="text" name="searchtag" className="searchtag_3" maxLength={30} placeholder="タグ名"/>
        {/* // } else { */}
        {/* //   <input type="text" name="searchtag" className="searchtag_3" maxLength={30} placeholder="タグ名" disabled/> */}
        {/* // } */}
        <div className="searchtag_n">
          <div className="searchtag_n_list">
          {/* for (searchtag in searchtag_list) {
            <a href="?search={{ searchtag.name }}" search={{ searchtag.name }}>{{ searchtag.name }}</a>
          } */}
          </div>
        </div>
        <label htmlFor="searchtag_add" className="searchtag_4"><span className="searchtag_center">完了</span></label>
        <div className="searchtag_left">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi bi-chevron-left" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
          </svg>
        </div>
        <div className="searchtag_right">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi bi-chevron-right" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
          </svg>
        </div>
      </form>
    </nav>
  )
}
