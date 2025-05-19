import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { UserNotificationOut } from 'types/internal/auth'
import { getSettingNotification } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getSettingNotification(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const userNotification = ret.value
  return { props: { userNotification, ...translations } }
}

interface Props {
  status: number
  userNotification: UserNotificationOut
}

export default function SettingNotificationPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingNotification {...props} />
    </ErrorCheck>
  )
}
