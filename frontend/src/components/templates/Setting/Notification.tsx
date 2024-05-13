import React, { useState } from 'react'
import { getNotification, postNotification } from 'api/user'
import { Notification, NotificationOut } from 'types/internal/auth'
import { isEmpty } from 'utils/constants/common'
import { notificationTypes } from 'utils/functions/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  notification: NotificationOut
}

export default function SettingNotification(props: Props) {
  const { notification } = props

  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [newNotification, setNewNotification] = useState<Notification>(notification)

  const handleToggle = (type: keyof Notification) => setNewNotification((prev) => ({ ...prev, [type]: !prev[type] }))

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    try {
      postNotification(newNotification)
    } catch (error) {
      setNewNotification(notification)
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancel = async () => {
    const data = await getNotification()
    setNewNotification(data)
  }

  return (
    <Main title="通知設定" type="table">
      <LoginRequired isAuth={!isEmpty(notification)}>
        <div className="button_group">
          <Button color="green" size="s" name="保存" loading={isLoading} onClick={handlSubmit} />
          <Button color="blue" size="s" name="キャンセル" onClick={handleCancel} />
        </div>

        <Table>
          <TableRow isIndent label="通知設定">
            フォローしているユーザの投稿通知などを設定
          </TableRow>
          {notificationTypes?.map((type, index) => (
            <TableRow key={index} isIndent label={`${type.slice(2)}通知`}>
              <form method="POST" action="">
                {newNotification && <Toggle isActive={newNotification[type]} onClick={() => handleToggle(type)} />}
              </form>
            </TableRow>
          ))}
        </Table>
      </LoginRequired>
    </Main>
  )
}
