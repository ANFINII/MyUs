import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerSettingNotification } from 'api/internal/setting'
import { UserNotificationOut } from 'types/internal/auth'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const userNotification = await getServerSettingNotification(req)
  return { props: { userNotification, ...translations } }
}

interface Props {
  userNotification: UserNotificationOut
}

export default function SettingNotificationPage(props: Props) {
  return <SettingNotification {...props} />
}
