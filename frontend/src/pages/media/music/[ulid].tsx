import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { MusicDetailOut } from 'types/internal/media/detail'
import { getMusic } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import MusicDetail from 'components/templates/media/music/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getMusic(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { ...translations, data } }
}

interface Props {
  status: number
  data: MusicDetailOut
}

export default function MusicDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <MusicDetail {...props} />
    </ErrorCheck>
  )
}
