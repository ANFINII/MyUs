import { user } from 'types/type'
import Main from 'components/layout/Main'
import Footer from 'components/layout/Footer'

interface notificationSetting {
  isVideo: boolean
  isMusic: boolean
  isComic: boolean
  isPicture: boolean
  isBlog: boolean
  isChat: boolean
  isFollow: boolean
  isReply: boolean
  isLike: boolean
  isViews: boolean
}

interface Props {
  user: user
  notificationSetting: notificationSetting
}

export default function Notification(props: Props) {
  const { user, notificationSetting } = props

  return (
    <Main title="MyUs通知">
      <article className="article_table">
        <h1>通知設定</h1>
        {user.isAuthenticated ? (
          <>
            <table id="notification_table" className="table">
              <tbody>
                <tr>
                  <td className="td_color">通知設定</td>
                  <td className="td_indent">フォローしているユーザの投稿通知などを設定</td>
                </tr>
                <tr>
                  <td className="td_color">Video通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isVideo }}" notification-type="video">
                      {notificationSetting.isVideo ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Music通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isMusic }}" notification-type="music">
                      {notificationSetting.isMusic ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Comic通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isComic }}" notification-type="comic">
                      {notificationSetting.isComic ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Picture通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isPicture }}" notification-type="picture">
                      {notificationSetting.isPicture ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Blog通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isBlog }}" notification-type="blog">
                      {notificationSetting.isBlog ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Chat通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isChat }}" notification-type="chat">
                      {notificationSetting.isChat ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">フォロー通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isFollow }}" notification-type="follow">
                      {notificationSetting.isFollow ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">返信通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isReply }}" notification-type="reply">
                      {notificationSetting.isReply ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">いいね通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isLike }}" notification-type="like">
                      {notificationSetting.isLike ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">閲覧数通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" data-notification="{{ notificationSetting.isViews }}" notification-type="views">
                      {notificationSetting.isViews ? (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-on toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                        </svg>
                      ) : (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="25"
                          height="25"
                          fill="currentColor"
                          className="bi-toggle-off toggle_button"
                          viewBox="0 0 16 16"
                        >
                          <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                        </svg>
                      )}
                    </form>
                  </td>
                </tr>
              </tbody>
            </table>

            <Footer />
          </>
        ) : (
          <h2 className="login_required">ログインしてください</h2>
        )}
      </article>
    </Main>
  )
}
