import { useState } from 'react'
import { putNotification, getNotification } from 'api/internal/user'
import { NotificationSetting, NotificationSettingOut } from 'types/internal/auth'
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
  notificationSetting: NotificationSettingOut
}

export default function SettingNotification(props: Props) {
  const { notificationSetting } = props

  const { user } = useUser()
  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [values, setValues] = useState<NotificationSetting>(notificationSetting)

  const handleToggle = (type: keyof NotificationSetting) => setValues((prev) => ({ ...prev, [type]: !prev[type] }))

  const handleSubmit = async () => {
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

  const buttonArea = (
    <>
      <Button color="green" size="s" name="保存" loading={isLoading} onClick={handleSubmit} />
      <Button color="blue" size="s" name="リセット" onClick={handleReset} />
    </>
  )

  return (
    <Main title="通知設定" type="table" toast={toast} buttonArea={buttonArea}>
      <LoginRequired isAuth={user.isActive}>
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
