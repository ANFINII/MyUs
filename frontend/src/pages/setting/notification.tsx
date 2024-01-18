import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getNotification } from 'api/user'
import { Notification } from 'types/internal/auth'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const notification = await getNotification(req)
  return { props: { notification, ...translations } }
}

interface Props {
  notification: Notification
}

export default function SettingNotificationPage(props: Props) {
  return <SettingNotification {...props} />
}
