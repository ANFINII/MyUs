import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Music } from 'types/internal/media'
import { getMusics } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Musics from 'components/templates/media/music/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const ret = await getMusics(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { ...translations, datas } }
}

interface Props {
  status: number
  datas: Music[]
}

export default function MusicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Musics {...props} />
    </ErrorCheck>
  )
}
