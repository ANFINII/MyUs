import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerSettingProfile } from 'api/internal/setting'
import { ProfileOut } from 'types/internal/auth'
import SettingProfileEdit from 'components/templates/setting/profile/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const profile = await getServerSettingProfile(req)
  return { props: { profile, ...translations } }
}

interface Props {
  profile: ProfileOut
}

export default function SettingProfilePage(props: Props) {
  return <SettingProfileEdit {...props} />
}
