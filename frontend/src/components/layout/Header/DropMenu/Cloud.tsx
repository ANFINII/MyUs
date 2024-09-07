import router from 'next/router'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import HeaderItem from './Item'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuCloud(props: Props) {
  const { open, onClose } = props

  const handleClick = (media: string) => {
    router.push(`/media/${media}/create`)
    onClose()
  }

  return (
    <nav className={clsx('drop_menu', 'drop_menu_cloud', isActive(open))}>
      <ul>
        <HeaderItem label="Videoアップロード" icon={<IconVideo size="1.5em" />} onClick={() => handleClick('video')} />
        <HeaderItem label="Musicアップロード" icon={<IconMusic size="1.5em" />} onClick={() => handleClick('music')} />
        <HeaderItem label="Comicアップロード" icon={<IconComic size="1.5em" />} onClick={() => handleClick('comic')} />
        <HeaderItem label="Pictureアップロード" icon={<IconPicture size="1.5em" />} onClick={() => handleClick('picture')} />
        <HeaderItem label="Blogアップロード" icon={<IconBlog size="1.5em" />} onClick={() => handleClick('blog')} />
        <HeaderItem label="Chatアップロード" icon={<IconChat size="1.5em" />} onClick={() => handleClick('chat')} />
      </ul>
    </nav>
  )
}
