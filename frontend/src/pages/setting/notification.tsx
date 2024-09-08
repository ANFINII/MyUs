import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerNotification } from 'api/internal/user'
import { NotificationSettingOut } from 'types/internal/auth'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const notificationSetting = await getServerNotification(req)
  return { props: { notificationSetting, ...translations } }
}

interface Props {
  notificationSetting: NotificationSettingOut
}

export default function NotificationSettingPage(props: Props) {
  return <SettingNotification {...props} />
}
