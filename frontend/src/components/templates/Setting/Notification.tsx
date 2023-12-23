import React, { useState } from 'react'
import { Notification } from 'types/internal/auth'
import Layout from 'components/layout'
import Toggle from 'components/parts/Input/Toggle'

interface Props {
  notification: Notification
}

export default function SettingNotification(props: Props) {
  const { notification } = props

  const [newNotificationSetting, setNewNotificationSetting] = useState<Notification>(notification)

  const notificationTypes: Array<keyof Notification> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
  const handleToggle = (type: keyof Notification) => setNewNotificationSetting((prev) => ({ ...prev, [type]: !prev[type] }))

  return (
    <Layout title="通知設定" type="table" isFooter>
      {notification ? (
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
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Layout>
  )
}
