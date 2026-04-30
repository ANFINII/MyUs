import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Advertise } from 'types/internal/advertise'
import { getManageAdvertises } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageAdvertises from 'components/templates/manage/advertise'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const advertisesRet = await getManageAdvertises({ search, limit, offset }, req)
  if (advertisesRet.isErr()) return { props: { status: advertisesRet.error.status } }
  const { datas, total } = advertisesRet.value
  return { props: { ...translations, datas, total, page } }
}

interface Props {
  status: number
  datas: Advertise[]
  total: number
  page: number
}

export default function ManageAdvertisesPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageAdvertises {...props} />
    </ErrorCheck>
  )
}
