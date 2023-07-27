import { useState } from 'react'
import { User } from 'types/auth'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Toggle from 'components/parts/Input/Toggle'

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
  user: User
  notificationSetting: notificationSetting
}

const user = {
  id: 1,
  nickname: 'anfinii',
  image: 'string',
  isAuthenticated: true,
}

const notificationSetting = {
  isVideo: true,
  isMusic: true,
  isComic: true,
  isPicture: true,
  isBlog: true,
  isChat: true,
  isFollow: true,
  isReply: true,
  isLike: true,
  isViews: true,
}

export default function Notification(props: Props) {
  // const { user, notificationSetting } = props

  const [isVideo, setIsVideo] = useState(notificationSetting.isVideo)
  const [isMusic, setIsMusic] = useState(notificationSetting.isMusic)
  const [isComic, setIsComic] = useState(notificationSetting.isComic)
  const [isPicture, setIsPicture] = useState(notificationSetting.isPicture)
  const [isBlog, setIsBlog] = useState(notificationSetting.isBlog)
  const [isChat, setIsChat] = useState(notificationSetting.isChat)
  const [isFollow, setIsFollow] = useState(notificationSetting.isFollow)
  const [isReply, setIsReply] = useState(notificationSetting.isReply)
  const [isLike, setIsLike] = useState(notificationSetting.isViews)
  const [isViews, setIsViews] = useState(notificationSetting.isViews)

  const handleToggle = (isState: boolean, stateSetter: React.Dispatch<boolean>) => stateSetter(!isState)

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
                    <form method="POST" action="" notification-type="video">
                      <Toggle isActive={isVideo} onClick={() => handleToggle(isVideo, setIsVideo)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Music通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="music">
                      <Toggle isActive={isMusic} onClick={() => handleToggle(isMusic, setIsMusic)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Comic通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="comic">
                      <Toggle isActive={isComic} onClick={() => handleToggle(isComic, setIsComic)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Picture通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="picture">
                      <Toggle isActive={isPicture} onClick={() => handleToggle(isPicture, setIsPicture)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Blog通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="blog">
                      <Toggle isActive={isBlog} onClick={() => handleToggle(isBlog, setIsBlog)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">Chat通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="chat">
                      <Toggle isActive={isChat} onClick={() => handleToggle(isChat, setIsChat)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">フォロー通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="follow">
                      <Toggle isActive={isFollow} onClick={() => handleToggle(isFollow, setIsFollow)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">返信通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="reply">
                      <Toggle isActive={isReply} onClick={() => handleToggle(isReply, setIsReply)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">いいね通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="like">
                      <Toggle isActive={isLike} onClick={() => handleToggle(isLike, setIsLike)} />
                    </form>
                  </td>
                </tr>
                <tr>
                  <td className="td_color">閲覧数通知</td>
                  <td className="td_indent">
                    <form method="POST" action="" notification-type="views">
                      <Toggle isActive={isViews} onClick={() => handleToggle(isViews, setIsViews)} />
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
