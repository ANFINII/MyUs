import { Channel } from 'types/internal/channel'
import Main from 'components/layout/Main'
import ChannelCard from 'components/widgets/Card/Channel'
import CardList from 'components/widgets/Card/List'

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
      <CardList items={datas} Content={ChannelCard} />
    </Main>
  )
}
