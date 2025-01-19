import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { ProfileOut } from 'types/internal/auth'
import { getSettingProfile } from 'api/internal/setting'
import SettingProfile from 'components/templates/setting/profile'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const profile = await getSettingProfile(req)
  return { props: { profile, ...translations } }
}

interface Props {
  profile: ProfileOut
}

export default function SettingProfilePage(props: Props): JSX.Element {
  return <SettingProfile {...props} />
}
