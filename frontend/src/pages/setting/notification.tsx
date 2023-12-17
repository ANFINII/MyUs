import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiNotification } from 'api/uri'
import { NotificationSetting } from 'types/internal/auth'
import Notification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const notificationSetting = async () => {
    await apiClient.get(apiNotification).then((res) => {
      return res.data
    })
  }
  return { props: { notificationSetting, ...translations } }
}

interface Props {
  notificationSetting: NotificationSetting
}

export default function NotificationPage(props: Props) {
  return <Notification {...props} />
}
