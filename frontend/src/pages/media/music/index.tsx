import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Music } from 'types/internal/media'
import { getMusics } from 'api/internal/media/list'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Musics from 'components/templates/media/music/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const ret = await getMusics(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Music[]
}

export default function MusicsPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Musics {...props} />
    </ErrorCheck>
  )
}
