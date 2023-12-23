import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { apiNotification } from 'api/uri'
import { Notification } from 'types/internal/auth'
import SettingNotification from 'components/templates/setting/notification'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const notification = await apiServer(req, apiClient, apiNotification).then((res) => {
    return res.data
  })
  return { props: { notification, ...translations } }
}

interface Props {
  notification: Notification
}

export default function SettingNotificationPage(props: Props) {
  return <SettingNotification {...props} />
}
