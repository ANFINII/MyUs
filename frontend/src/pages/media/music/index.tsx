import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Music } from 'types/internal/media'
import { getMusics } from 'api/internal/media/list'
import Musics from 'components/templates/media/music/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getMusics()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Music[]
}

export default function MusicsPage(props: Props): JSX.Element {
  return <Musics {...props} />
}
