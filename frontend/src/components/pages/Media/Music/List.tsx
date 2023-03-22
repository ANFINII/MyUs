import {Query, MusicResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleMusic from 'components/elements/Article/Music'

interface Props {
  query?: Query
  datas: Array<MusicResponse>
}

export default function MusicList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsミュージック" hero="Music" query={query}>
      <ArticleMusic datas={datas} />
    </Main>
  )
}
