import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { ProfileOut } from 'types/internal/auth'
import { getSettingProfile } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import SettingProfile from 'components/templates/setting/profile'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getSettingProfile(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const profile = ret.value
  return { props: { profile, ...translations } }
}

interface Props {
  status: number
  profile: ProfileOut
}

export default function SettingProfilePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingProfile {...props} />
    </ErrorCheck>
  )
}
