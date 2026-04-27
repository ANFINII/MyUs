import router from 'next/router'
import cx from 'utils/functions/cx'
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
        <NavItem label="投稿管理" icon={<IconGrid size="1.5em" />} className={style.item} onClick={() => handleManage()} />
        <NavItem label="Videoアップロード" icon={<IconVideo size="1.5em" />} className={style.item} onClick={() => handleRouter('video')} />
        <NavItem label="Musicアップロード" icon={<IconMusic size="1.5em" />} className={style.item} onClick={() => handleRouter('music')} />
        <NavItem label="Blogアップロード" icon={<IconBlog size="1.5em" />} className={style.item} onClick={() => handleRouter('blog')} />
        <NavItem label="Comicアップロード" icon={<IconComic size="1.5em" />} className={style.item} onClick={() => handleRouter('comic')} />
        <NavItem label="Pictureアップロード" icon={<IconPicture size="1.5em" />} className={style.item} onClick={() => handleRouter('picture')} />
        <NavItem label="Chatアップロード" icon={<IconChat size="1.5em" />} className={style.item} onClick={() => handleRouter('chat')} />
      </ul>
    </nav>
  )
}
