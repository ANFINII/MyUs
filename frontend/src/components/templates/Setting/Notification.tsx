import React, { useState } from 'react'
import { Notification } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  notification: Notification
}

export default function SettingNotification(props: Props) {
  const { notification } = props

  const [newNotificationSetting, setNewNotificationSetting] = useState<Notification>(notification)

  const notificationTypes: Array<keyof Notification> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
  const handleToggle = (type: keyof Notification) => setNewNotificationSetting((prev) => ({ ...prev, [type]: !prev[type] }))

  return (
    <Main title="通知設定" type="table">
      <LoginRequired isAuth={!!notification}>
        <table id="notification_table" className="table">
          <tbody>
            <tr>
              <td className="td_color">通知設定</td>
              <td className="td_indent">フォローしているユーザの投稿通知などを設定</td>
            </tr>
            {notificationTypes.map((type) => (
              <tr key={type}>
                <td className="td_color">{`${type.slice(2)}通知`}</td>
                <td className="td_indent">
                  <form method="POST" action="" Notification-type={type}>
                    <Toggle isActive={newNotificationSetting[type]} onClick={() => handleToggle(type)} />
                  </form>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </LoginRequired>
    </Main>
  )
}
