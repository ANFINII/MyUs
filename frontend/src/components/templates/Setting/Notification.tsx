import React, { useState } from 'react'
import { getNotification, putNotification } from 'api/user'
import { Notification, NotificationOut } from 'types/internal/auth'
import { notificationTypes } from 'utils/functions/user'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
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

  const { user } = useUser()
  const { toastContent, isError, isToast, setIsToast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [values, setValues] = useState<Notification>(notification)

  const handleToggle = (type: keyof Notification) => setValues((prev) => ({ ...prev, [type]: !prev[type] }))

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    try {
      await putNotification(values)
    } catch (e) {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = async () => {
    const data = await getNotification()
    setValues(data)
  }

  return (
    <Main title="通知設定" type="table" toast={{ toastContent, isError, isToast, setIsToast }}>
      <LoginRequired isAuth={user.isActive}>
        <div className="button_group">
          <Button color="green" size="s" name="保存" loading={isLoading} onClick={handlSubmit} />
          <Button color="blue" size="s" name="リセット" onClick={handleReset} />
        </div>

        <Table>
          <TableRow isIndent label="通知設定">
            フォローしているユーザの投稿通知などを設定
          </TableRow>
          {notificationTypes?.map((type, index) => (
            <TableRow key={index} isIndent label={`${type.slice(2)}通知`}>
              <Toggle isActive={values[type]} onClick={() => handleToggle(type)} />
            </TableRow>
          ))}
        </Table>
      </LoginRequired>
    </Main>
  )
}
