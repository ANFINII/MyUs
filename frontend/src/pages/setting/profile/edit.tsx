import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { ProfileOut } from 'types/internal/auth'
import { getSettingProfile } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import SettingProfileEdit from 'components/templates/setting/profile/edit'

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

export default function SettingProfilePage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingProfileEdit {...props} />
    </ErrorCheck>
  )
}
