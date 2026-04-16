import router from 'next/router'
import cx from 'utils/functions/cx'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import MenuItem from 'components/parts/NavItem/MenuItem'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuCloud(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const handleRouter = (media: string) => {
    router.push(`/manage/${media}/create`)
    onClose()
  }

  return (
    <nav className={cx(style.drop_menu, open && style.active)}>
      <ul>
        <MenuItem label="Videoアップロード" icon={<IconVideo size="1.5em" />} className={style.item} onClick={() => handleRouter('video')} />
        <MenuItem label="Musicアップロード" icon={<IconMusic size="1.5em" />} className={style.item} onClick={() => handleRouter('music')} />
        <MenuItem label="Comicアップロード" icon={<IconComic size="1.5em" />} className={style.item} onClick={() => handleRouter('comic')} />
        <MenuItem label="Pictureアップロード" icon={<IconPicture size="1.5em" />} className={style.item} onClick={() => handleRouter('picture')} />
        <MenuItem label="Blogアップロード" icon={<IconBlog size="1.5em" />} className={style.item} onClick={() => handleRouter('blog')} />
        <MenuItem label="Chatアップロード" icon={<IconChat size="1.5em" />} className={style.item} onClick={() => handleRouter('chat')} />
      </ul>
    </nav>
  )
}
