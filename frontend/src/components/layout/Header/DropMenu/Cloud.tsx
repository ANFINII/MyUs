import router from 'next/router'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import DropMenuItem from 'components/parts/NavItem/DropMenuItem'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuCloud(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const handleClick = (media: string) => {
    router.push(`/media/${media}/create`)
    onClose()
  }

  return (
    <nav className={clsx('drop_menu drop_menu_cloud', isActive(open))}>
      <ul>
        <DropMenuItem label="Videoアップロード" icon={<IconVideo size="1.5em" />} onClick={() => handleClick('video')} />
        <DropMenuItem label="Musicアップロード" icon={<IconMusic size="1.5em" />} onClick={() => handleClick('music')} />
        <DropMenuItem label="Comicアップロード" icon={<IconComic size="1.5em" />} onClick={() => handleClick('comic')} />
        <DropMenuItem label="Pictureアップロード" icon={<IconPicture size="1.5em" />} onClick={() => handleClick('picture')} />
        <DropMenuItem label="Blogアップロード" icon={<IconBlog size="1.5em" />} onClick={() => handleClick('blog')} />
        <DropMenuItem label="Chatアップロード" icon={<IconChat size="1.5em" />} onClick={() => handleClick('chat')} />
      </ul>
    </nav>
  )
}
