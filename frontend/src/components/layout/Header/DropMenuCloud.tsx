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
      <label className="drop_back_cover"></label>
      <label className="drop_open">
        <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-cloud-fill" viewBox="0 0 16 16">
          <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z" />
        </svg>
      </label>

      {isOpen && (
        <nav className={`drop_menu drop_menu_cloud ${isOpen && 'active'}`}>
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
      )}
    </>
  )
}
