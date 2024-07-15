import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerProfile } from 'api/user'
import { ProfileOut } from 'types/internal/auth'
import SettingProfile from 'components/templates/setting/profile'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const profile = await getServerProfile(req)
  return { props: { profile, ...translations } }
}

interface Props {
  profile: ProfileOut
}

export default function SettingProfilePage(props: Props) {
  return <SettingProfile {...props} />
}
