import Link from 'next/link'

export default function DropMenuNotice() {
  return (
    <>
      <input type="checkbox" id="drop_menu_notice" className="drop_menu_notice" />
      <label htmlFor="drop_menu_notice" className="drop_back_cover"></label>
      <label htmlFor="drop_menu_notice" className="drop_open">
        {/* if (notification_count) {
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-bell-fill active" viewBox="0 0 16 16">
            <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
          </svg>
          <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" fill="currentColor" className="bi bi-exclamation-lg active" viewBox="0 0 16 16">
            <path d="M7.005 3.1a1 1 0 1 1 1.99 0l-.388 6.35a.61.61 0 0 1-1.214 0L7.005 3.1ZM7 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z"/>
          </svg>
        } else { */}
        <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-bell-fill" viewBox="0 0 16 16">
          <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z" />
        </svg>
        {/* <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" fill="currentColor" className="bi bi-exclamation-lg" viewBox="0 0 16 16">
            <path d="M7.005 3.1a1 1 0 1 1 1.99 0l-.388 6.35a.61.61 0 0 1-1.214 0L7.005 3.1ZM7 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z"/>
          </svg>
        } */}
      </label>

      <nav className="drop_menu drop_menu_notice">
        <ul>
          <li className="drop_menu_list">
            <Link href="/setting/notification" className="icon_link"></Link>
            <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-bell-fill color_drop_menu_bi" viewBox="0 0 16 16">
              <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z" />
            </svg>
            <span>通知設定</span>
          </li>

          {/* {% for notification in notification_list %} */}
          <li id="notification_aria_link_{{ notification.id }}" className="drop_menu_list">
            <object notification-id="{{ notification.id }}" data-csrf="{{ csrf_token }}" className="notification_aria_list">
              {/* <a href="{% url 'myus:userpage' notification.user_from.nickname %}" data-notification="{{ notification.user_from.nickname }}">
                <img src="{{ notification.user_from.image }}" title="{{ notification.user_from.nickname }}" className="profile_image"/>
              </a> */}
              {/* {% if notification.user_confirmed %} */}
              <span></span>
              {/* {% else %} */}
              <svg xmlns="http://www.w3.org/2000/svg" className="svg-circle" viewBox="0 0 2 2">
                <circle cx="1" cy="1" r="1"></circle>
              </svg>
              {/* {% endif %} */}

              {/* {% if notification.type_name == 'video' %} */}
              {/* <a href="{% url 'myus:video_detail' notification.content_object.id notification.content_object.title %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_name == 'music' %} */}
              {/* <a href="{% url 'myus:music_detail' notification.content_object.id notification.content_object.title %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_name == 'comic' %} */}
              {/* <a href="{% url 'myus:comic_detail' notification.content_object.id notification.content_object.title %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_name == 'picture' %} */}
              {/* <a href="{% url 'myus:picture_detail' notification.content_object.id notification.content_object.title %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_name == 'blog' %} */}
              {/* <a href="{% url 'myus:blog_detail' notification.content_object.id notification.content_object.title %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_name == 'chat' %} */}
              {/* <a href="{% url 'myus:chat_detail' notification.content_object.id %}" className="notification_aria_anker"> */}
              {/* {% elif notification.type_no >= 8 and notification.type_no <= 10 %} */}
              {/* <a href="{% url 'myus:userpage' notification.user_from.nickname %}" data="{{ notification.user_from.nickname }}" className="notification_aria_anker pjax_button_userpage"> */}
              {/* {% endif %} */}
              {/* {% if notification.type_no >= 1 and notification.type_no <= 7 %} */}
              <div className="notification_aria_list_1" title="{{ notification.user_from.nickname }}さんが{{ notification.content_object.title }}を投稿しました">
                {/* {{ notification.content_object.title }} */}
              </div>
              {/* {% elif notification.type_no == 8 %} */}
              <div className="notification_aria_list_1" title="{{ notification.user_from.nickname }}さんにフォローされました">
                {/* {{ notification.user_from.nickname }}さんにフォローされました */}
              </div>
              {/* {% elif notification.type_no == 9 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.text }}が{{ notification.user_from.nickname }}さんにいいねされました">
                {/* {{ notification.content_object.text }}が{{ notification.user_from.nickname }}さんにいいねされました */}
              </div>
              {/* {% elif notification.type_no == 10 %} */}
              <div className="notification_aria_list_1" title="{{ notification.user_from.nickname }}さんから返信がありました {{ notification.content_object.text }}">
                {/* {{ notification.content_object.text }} */}
              </div>
              {/* {% elif notification.type_no == 11 %} */}
              {/* {% if  notification.content_object.read >= 1000000000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が10億回閲覧されました">
                {/* {{ notification.content_object.title }}が10億回閲覧されました */}
              </div>
              {/* {% elif  notification.content_object.read >= 100000000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が1億回閲覧されました">
                {/* {{ notification.content_object.title }}が1億回閲覧されました */}
              </div>
              {/* {% elif  notification.content_object.read >= 10000000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が1000万回閲覧されました">
                {/* {{ notification.content_object.title }}が1000万回閲覧されました */}
              </div>
              {/* {% elif  notification.content_object.read >= 1000000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が100万回閲覧されました">
                {/* {{ notification.content_object.title }}が100万回閲覧されました */}
              </div>
              {/* {% elif  notification.content_object.read >= 100000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が10万回閲覧されました">
                {/* {{ notification.content_object.title }}が10万回閲覧されました */}
              </div>
              {/* {% elif  notification.content_object.read >= 10000 %} */}
              <div className="notification_aria_list_1" title="{{ notification.content_object.title }}が1万回閲覧されました">
                {/* {{ notification.content_object.title }}が1万回閲覧されました */}
              </div>
              {/* {% endif %} */}
              {/* {% endif %} */}
              {/* </a> */}

              <form method="POST" action="">
                {/* <i title="閉じる" className="bi-x notification_aria_list_2" style={{font-size: '1.41em';}}></i> */}
              </form>
            </object>
          </li>
          {/* {% endfor %} */}
        </ul>
      </nav>
    </>
  )
}
