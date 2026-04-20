import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { PictureDetailOut } from 'types/internal/media/output'
import { getPicture } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import PictureDetail from 'components/templates/media/picture/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getPicture(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { ...translations, data } }
}

interface Props {
  status: number
  data: PictureDetailOut
}

export default function PictureDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <PictureDetail {...props} />
    </ErrorCheck>
  )
}
