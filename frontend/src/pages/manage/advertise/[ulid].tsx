import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Advertise } from 'types/internal/advertise'
import { getManageAdvertise } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageAdvertiseEdit from 'components/templates/manage/advertise/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const advertiseRet = await getManageAdvertise(ulid, req)
  if (advertiseRet.isErr()) return { props: { status: advertiseRet.error.status } }
  const data = advertiseRet.value
  return { props: { ...translations, data } }
}

interface Props {
  status: number
  data: Advertise
}

export default function ManageAdvertiseEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageAdvertiseEdit {...props} />
    </ErrorCheck>
  )
}
