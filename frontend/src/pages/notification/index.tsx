import Head from 'next/head'
import Footer from 'components/layouts/Footer'

export default function Notification() {
  return (
    <>
      <Head>
        <title>MyUs通知</title>
      </Head>

      <article className="article_account">
        <h1>通知設定</h1>
        {/* {% if user.is_authenticated %}
        {% for notification in notification_setting_list %} */}
        <table id="notification_table" data-csrf="{{ csrf_token }}" className="table">
          <tbody>
            <tr><td className="td_color">通知設定</td><td className="td-indent">フォローしているユーザの投稿通知などを設定</td></tr>
            <tr><td className="td_color">Video通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_video }}" notification-type="video">
                {/* {% if notification.is_video %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">Music通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_music }}" notification-type="music">
                {/* {% if notification.is_music %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">Picture通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_picture }}"  notification-type="picture">
                {/* {% if notification.is_picture %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">Blog通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_blog }}" notification-type="blog">
                {/* {% if notification.is_blog %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">Chat通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_chat }}" notification-type="chat">
                {/* {% if notification.is_chat %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">Collabo通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_collabo }}" notification-type="collabo">
                {/* {% if notification.is_collabo %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">フォロー通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_follow }}" notification-type="follow">
                {/* {% if notification.is_follow %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">返信通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_reply }}" notification-type="reply">
                {/* {% if notification.is_reply %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">いいね通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_like }}" notification-type="like">
                {/* {% if notification.is_like %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
            <tr><td className="td_color">閲覧数通知</td><td className="td-indent">
              <form method="POST" action="" data-notification="{{ notification.is_views }}" notification-type="views">
                {/* {% if notification.is_views %} */}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_button" viewBox="0 0 16 16">
                  <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                </svg>
                {/* {% else %}
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_button" viewBox="0 0 16 16">
                  <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                </svg>
                {% endif %} */}
              </form>
            </td></tr>
          </tbody>
        </table>
        {/* {% endfor %} */}

        <Footer/>
        {/* {% else %}
        <h2 className="login_required">ログインしてください</h2>
        {% endif %} */}
      </article>
    </>
  )
}
