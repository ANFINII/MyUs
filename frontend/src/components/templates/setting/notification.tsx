import { useState } from 'react'
import { getSettingNotification, putSettingNotification } from 'api/internal/setting'
import { UserNotification, UserNotificationOut } from 'types/internal/auth'
import { notificationTypes } from 'utils/functions/user'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Horizontal from 'components/parts/Horizontal/inedex'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  userNotification: UserNotificationOut
}

export default function SettingNotification(props: Props) {
  const { userNotification } = props

  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [values, setValues] = useState<UserNotification>(userNotification)

  const handleToggle = (type: keyof UserNotification) => setValues((prev) => ({ ...prev, [type]: !prev[type] }))

  const handleSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    try {
      await putSettingNotification(values)
    } catch (e) {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = async () => {
    const data = await getSettingNotification()
    setValues(data)
  }

  const buttonArea = (
    <Horizontal gap="4">
      <Button color="green" size="s" name="保存" loading={isLoading} onClick={handleSubmit} />
      <Button color="blue" size="s" name="リセット" onClick={handleReset} />
    </Horizontal>
  )

  return (
    <Main title="通知設定" type="table" toast={toast} buttonArea={buttonArea}>
      <LoginRequired>
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
