import { useRouter } from 'next/router'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'

interface Props {
  isOpen: boolean
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export default function DropMenuCloud(props: Props) {
  const { isOpen, setIsOpen } = props

  const router = useRouter()

  const handleClick = (url: string) => {
    router.push(url)
    setIsOpen(false)
  }

  return (
    <>
      <nav className={'drop_menu drop_menu_cloud' + (isOpen ? ' ' + 'active' : '')}>
        <ul>
          <li className="drop_menu_list" onClick={() => handleClick('/media/video/create')}>
            <IconVideo size="1.5em" className="color_drop_menu_bi" />
            <span>Videoアップロード</span>
          </li>

          <li className="drop_menu_list" onClick={() => handleClick('/media/music/create')}>
            <IconMusic size="1.5em" className="color_drop_menu_bi" />
            <span>Musicアップロード</span>
          </li>

          <li className="drop_menu_list" onClick={() => handleClick('/media/comic/create')}>
            <IconComic size="1.5em" className="color_drop_menu_bi" />
            <span>Comicアップロード</span>
          </li>

          <li className="drop_menu_list" onClick={() => handleClick('/media/picture/create')}>
            <IconPicture size="1.5em" className="color_drop_menu_bi" />
            <span>Pictureアップロード</span>
          </li>

          <li className="drop_menu_list" onClick={() => handleClick('/media/blog/create')}>
            <IconBlog size="1.5em" className="color_drop_menu_bi" />
            <span>Blogアップロード</span>
          </li>

          <li className="drop_menu_list" onClick={() => handleClick('/media/chat/create')}>
            <IconChat size="1.5em" className="color_drop_menu_bi" />
            <span>Chatアップロード</span>
          </li>
        </ul>
      </nav>
    </>
  )
}
