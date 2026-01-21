import { useState } from 'react'
import { UserNotification, UserNotificationOut } from 'types/internal/user'
import { getSettingNotification, putSettingNotification } from 'api/internal/setting'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Toggle from 'components/parts/Input/Toggle'
import HStack from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  userNotification: UserNotificationOut
}

export default function SettingNotification(props: Props): React.JSX.Element {
  const { userNotification } = props

  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const [values, setValues] = useState<UserNotification>(userNotification)

  const handleToggle = (key: keyof UserNotification) => setValues((prev) => ({ ...prev, [key]: !prev[key] }))

  const handleSubmit = async () => {
    handleLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const ret = await putSettingNotification(values)
    if (ret.isErr()) {
      handleLoading(false)
      handleToast(FetchError.Put, true)
      return
    }
    handleLoading(false)
    handleToast(Fetch.Save, false)
  }

  const handleReset = async () => {
    const ret = await getSettingNotification()
    if (ret.isErr()) return handleToast(FetchError.Get, true)
    setValues(ret.value)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name="保存" loading={isLoading} onClick={handleSubmit} />
      <Button color="blue" size="s" name="リセット" onClick={handleReset} />
    </HStack>
  )

  return (
    <Main title="通知設定" type="table" toast={toast} button={button}>
      <LoginError>
        <Table>
          <TableRow isIndent label="通知設定">
            フォローしているユーザの投稿通知などを設定
          </TableRow>
          {Object.keys(userNotification).map((key) => (
            <TableRow key={key} isIndent label={`${key.slice(2)}通知`}>
              <Toggle isActive={values[key as keyof UserNotification]} onClick={() => handleToggle(key as keyof UserNotification)} />
            </TableRow>
          ))}
        </Table>
      </LoginError>
    </Main>
  )
}
