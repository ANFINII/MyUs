import React, { useState } from 'react'
import { Notification } from 'types/internal/auth'
import { notificationTypes } from 'utils/functions/user'
import Main from 'components/layout/Main'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  notification: Notification
}

export default function SettingNotification(props: Props) {
  const { notification } = props

  const [newNotification, setNewNotification] = useState<Notification>(notification)

  const handleToggle = (type: keyof Notification) => setNewNotification((prev) => ({ ...prev, [type]: !prev[type] }))

  return (
    <Main title="通知設定" type="table">
      <LoginRequired isAuth={!!notification}>
        <Table>
          <TableRow isIndent label="通知設定">
            フォローしているユーザの投稿通知などを設定
          </TableRow>
          {notificationTypes.map((type) => (
            <TableRow isIndent label={`${type.slice(2)}通知`} key={type}>
              <form method="POST" action="">
                <Toggle isActive={newNotification[type]} onClick={() => handleToggle(type)} />
              </form>
            </TableRow>
          ))}
        </Table>
      </LoginRequired>
    </Main>
  )
}
