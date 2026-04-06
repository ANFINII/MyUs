import { Channel } from 'types/internal/channel'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaChannel from 'components/widgets/Menu/Channel'

interface Props {
  datas: Channel[]
}

export default function Channels(props: Props): React.JSX.Element {
  const { datas } = props

  return (
    <Main title="Channel">
      <div className="mt_16">
        <span>登録チャンネル数：{datas.length}</span>
      </div>
      <MediaList medias={datas} MediaComponent={MediaChannel} />
    </Main>
  )
}
