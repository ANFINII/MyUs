import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { ComicDetailOut } from 'types/internal/media/detail'
import { getComic } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import ComicDetail from 'components/templates/media/comic/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getComic(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { ...translations, data } }
}

interface Props {
  status: number
  data: ComicDetailOut
}

export default function ComicDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ComicDetail {...props} />
    </ErrorCheck>
  )
}
