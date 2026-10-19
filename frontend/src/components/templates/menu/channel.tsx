import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import Main from 'components/layout/Main'
import ChannelCard from 'components/widgets/Card/Channel'
import CardList from 'components/widgets/Card/List'

interface Props {
  data: Channel[]
}

export default function Channels(props: Props): React.JSX.Element {
  const { data } = props

  const { t } = useTranslation()

  return (
    <Main title="Channel">
      <div className="mt_16">
        <span>{t('menu.channel.count', { count: data.length })}</span>
      </div>
      <CardList items={data} Content={ChannelCard} />
    </Main>
  )
}
