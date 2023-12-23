import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { apiProfile } from 'api/uri'
import { UserProfile } from 'types/internal/auth'
import SettingProfile from 'components/templates/setting/profile'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const user = await apiServer(req, apiClient, apiProfile).then((res) => {
    return res.data
  })
  return { props: { user, ...translations } }
}

interface Props {
  user: UserProfile
}

export default function SettingProfilePage(props: Props) {
  return <SettingProfile {...props} />
}
