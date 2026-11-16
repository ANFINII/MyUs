import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Tabs, { TabItem } from 'components/parts/Tabs'
import style from './MusicTabs.module.scss'

type MusicTabKey = 'all' | 'playlist'

const paths: Record<MusicTabKey, string> = {
  all: '/media/music',
  playlist: '/media/music/playlist',
}

interface Props {
  selected: MusicTabKey
}

export default function MusicTabs(props: Props): React.JSX.Element {
  const { selected } = props

  const router = useRouter()
  const { t } = useTranslation()

  const items: TabItem<MusicTabKey>[] = [
    { key: 'all', label: t('playlist.tabAll') },
    { key: 'playlist', label: t('playlist.tabPlaylist') },
  ]

  const handleSelect = (key: MusicTabKey) => router.push(paths[key])

  return (
    <div className={style.tabs}>
      <Tabs items={items} selected={selected} onSelect={handleSelect} />
    </div>
  )
}
