import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiMusics } from 'api/uri'
import { Music } from 'types/internal/media'
import Musics from 'components/templates/media/music/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await apiClient.get(apiMusics).then((res) => {
    return res.data
  })
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Music[]
}

export default function MusicsPage(props: Props) {
  return <Musics {...props} />
}
