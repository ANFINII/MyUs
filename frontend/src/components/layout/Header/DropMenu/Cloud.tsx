import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useUser } from 'components/hooks/useUser'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconGrid from 'components/parts/Icon/Grid'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import NavItem from 'components/parts/NavItem'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuCloud(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const router = useAppRouter()
  const { t } = useTranslation()
  const { user } = useUser()

  const handleManage = () => {
    if (user.isStaff) router.push('http://127.0.0.1:8000/myus-admin')
    router.push('/manage')
    onClose()
  }

  const handleRouter = (media: string) => {
    router.push(`/manage/${media}/create`)
    onClose()
  }

  return (
    <nav className={cx(style.drop_menu, open && style.active)}>
      <ul>
        <NavItem label={t('cloudMenu.manage')} icon={<IconGrid size="1.5em" />} className={style.item} onClick={() => handleManage()} />
        <NavItem label={t('cloudMenu.upload', { media: 'Video' })} icon={<IconVideo size="1.5em" />} className={style.item} onClick={() => handleRouter('video')} />
        <NavItem label={t('cloudMenu.upload', { media: 'Music' })} icon={<IconMusic size="1.5em" />} className={style.item} onClick={() => handleRouter('music')} />
        <NavItem label={t('cloudMenu.upload', { media: 'Blog' })} icon={<IconBlog size="1.5em" />} className={style.item} onClick={() => handleRouter('blog')} />
        <NavItem label={t('cloudMenu.upload', { media: 'Comic' })} icon={<IconComic size="1.5em" />} className={style.item} onClick={() => handleRouter('comic')} />
        <NavItem label={t('cloudMenu.upload', { media: 'Picture' })} icon={<IconPicture size="1.5em" />} className={style.item} onClick={() => handleRouter('picture')} />
        <NavItem label={t('cloudMenu.upload', { media: 'Chat' })} icon={<IconChat size="1.5em" />} className={style.item} onClick={() => handleRouter('chat')} />
      </ul>
    </nav>
  )
}
