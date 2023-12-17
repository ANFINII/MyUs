import React, { useState } from 'react'
import { NotificationSetting } from 'types/internal/auth'
import Layout from 'components/layout'
import Toggle from 'components/parts/Input/Toggle'

interface Props {
  // user?: boolean
  notificationSetting: NotificationSetting
}

export default function Notification(props: Props) {
  const { notificationSetting } = props

  const user = {}

  const [newNotificationSetting, setNewNotificationSetting] = useState<NotificationSetting>(notificationSetting)

  const notificationTypes: Array<keyof NotificationSetting> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
  const handleToggle = (type: keyof NotificationSetting) => setNewNotificationSetting((prev) => ({ ...prev, [type]: !prev[type] }))

  return (
    <Layout title="通知設定" type="table" isFooter>
      {user ? (
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
                  <form method="POST" action="" notification-type={type}>
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
