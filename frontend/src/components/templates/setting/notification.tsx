import { useState } from 'react'
import { UserNotification, UserNotificationOut } from 'types/internal/auth'
import { getSettingNotification, putSettingNotification } from 'api/internal/setting'
import { notificationTypes } from 'utils/functions/user'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Toggle from 'components/parts/Input/Toggle'
import Horizontal from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  userNotification: UserNotificationOut
}

export default function SettingNotification(props: Props): JSX.Element {
  const { userNotification } = props

  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [values, setValues] = useState<UserNotification>(userNotification)

  const handleToggle = (type: keyof UserNotification) => setValues((prev) => ({ ...prev, [type]: !prev[type] }))

  const handleSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const ret = await putSettingNotification(values)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast('エラーが発生しました！', true)
      return
    }
    setIsLoading(false)
  }

  const handleReset = async () => {
    const ret = await getSettingNotification()
    if (ret.isErr()) return handleToast('エラーが発生しました！', true)
    setValues(ret.value)
  }

  const button = (
    <Horizontal gap="4">
      <Button color="green" size="s" name="保存" loading={isLoading} onClick={handleSubmit} />
      <Button color="blue" size="s" name="リセット" onClick={handleReset} />
    </Horizontal>
  )

  return (
    <Main title="通知設定" type="table" toast={toast} button={button}>
      <LoginError>
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
      </LoginError>
    </Main>
  )
}
