import Link from 'next/link'

export default function DropMenuProfile() {
  return (
    <>
      <input type="checkbox" id="drop_menu_profile" className="drop_menu_profile"/>
      <label htmlFor="drop_menu_profile" className="drop_open_profile">
        {/* if (user.is_authenticated) { */}
          {/* <img src="img/user.image" title="{{ user.nickname }}" width="32px" height="32xp"/> */}
        {/* } else { */}
          <img src="img/user_icon.png" title="匿名" width="32px" height="32xp"/>
        {/* } */}
      </label>
      <label htmlFor="drop_menu_profile" className="drop_back_profile"></label>

      <nav className="drop_menu_profile">
        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-person-circle color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
          </svg>
          <div>アカウント</div>
          <Link href="/profile">
            <a className="icon_link" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-person-square color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z"/>
          </svg>
          <div>Myページ</div>
          <Link href="/mypage">
            <a className="icon_link" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-grid color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z"/>
          </svg>
          <div>投稿管理</div>
          {/* if (user.is_staff) {
            <Link href="/">
              <a className="icon_link" role="button" aria-disabled="true"></a>
            </Link>
          } elif (user.is_active) {
            <Link href="/">
              <a className="icon_link" role="button" aria-disabled="true"></a>
            </Link>
          } else { */}
            <Link href="/login">
              <a className="icon_link" role="button" aria-disabled="true"></a>
            </Link>
          {/* } */}
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-pencil-square color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
          </svg>
          <div>ToDo</div>
          <Link href="/todo">
            <a className="icon_link" role="button" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-credit-card color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v1h14V4a1 1 0 0 0-1-1H2zm13 4H1v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V7z"/>
            <path d="M2 10a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-1z"/>
          </svg>
          <div>料金プラン</div>
          <Link href="/payment">
            <a className="icon_link" role="button" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-person-x color_drop_menu_bi" viewBox="0 0 16 16">
            <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
            <path fill-rule="evenodd" d="M12.146 5.146a.5.5 0 0 1 .708 0L14 6.293l1.146-1.147a.5.5 0 0 1 .708.708L14.707 7l1.147 1.146a.5.5 0 0 1-.708.708L14 7.707l-1.146 1.147a.5.5 0 0 1-.708-.708L13.293 7l-1.147-1.146a.5.5 0 0 1 0-.708z"/>
          </svg>
          <div>退会処理</div>
          {/* if (user.is_staff) {
            <a className="icon_link" role="button" aria-disabled="true"></a>
          } else { */}
            <Link href="/withdrawal">
              <a className="icon_link" aria-disabled="true"></a>
            </Link>
          {/* } */}
        </div>

        <div className="drop_menu_item side_nemu_indent color_drop_menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-box-arrow-right color_drop_menu_bi" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
            <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
          </svg>
          <div>ログアウト</div>
          {/* if (user.is_authenticated) {
            <Link href="/logout">
              <a className="icon_link" role="button" aria-disabled="true"></a>
            </Link>
          } else { */}
            <Link href="/login">
              <a className="icon_link" role="button" aria-disabled="true"></a>
            </Link>
          {/* } */}
        </div>
      </nav>
    </>
  )
}
