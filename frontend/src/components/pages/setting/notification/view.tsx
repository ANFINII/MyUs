import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { UserNotification, UserNotificationOut } from 'types/internal/user'
import { getSettingNotification, putSettingNotification } from 'api/internal/setting'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Toggle from 'components/parts/Input/Toggle'
import HStack from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  userNotification: UserNotificationOut
}

export default function SettingNotification(props: Props): React.JSX.Element {
  const { userNotification } = props

  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
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

  const notificationKeys: (keyof UserNotification)[] = ['isVideo', 'isMusic', 'isBlog', 'isComic', 'isPicture', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('setting.button.save')} loading={loading} onClick={handleSubmit} />
      <Button color="blue" size="s" name={t('setting.button.reset')} onClick={handleReset} />
    </HStack>
  )

  return (
    <Main title={t('setting.notification.title')} type="table" toast={toast} button={button}>
      <Table>
        <TableRow isIndent label={t('setting.notification.title')}>
          {t('setting.notification.description')}
        </TableRow>
        {notificationKeys.map((key) => (
          <TableRow key={key} isIndent label={t('setting.notification.item', { name: key.slice(2) })}>
            <Toggle isActive={values[key]} onClick={() => handleToggle(key)} />
          </TableRow>
        ))}
      </Table>
    </Main>
  )
}
