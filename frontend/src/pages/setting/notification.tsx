import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerNotification } from 'api/internal/user'
import { NotificationOut } from 'types/internal/auth'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const notification = await getServerNotification(req)
  return { props: { notification, ...translations } }
}

interface Props {
  notification: NotificationOut
}

export default function SettingNotificationPage(props: Props) {
  return <SettingNotification {...props} />
}
