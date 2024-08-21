import { useRouter } from 'next/router'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'

export default function SideBar() {
  const router = useRouter()

  const handleClick = (url: string) => router.push(url)
  const activeCheck = (url: string) => isActive(router.pathname === url)

  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <li className={clsx('sidebar_color', activeCheck('/media/video'))}>
            <div onClick={() => handleClick('/media/video')}>
              <IconVideo size="1.8em" />
              <p className="sidebar_text">Video</p>
            </div>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/music'))}>
            <div onClick={() => handleClick('/media/music')}>
              <IconMusic size="1.8em" />
              <p className="sidebar_text">Music</p>
            </div>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/comic'))}>
            <div onClick={() => handleClick('/media/comic')}>
              <IconComic size="1.8em" />
              <p className="sidebar_text">Comic</p>
            </div>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/picture'))}>
            <div onClick={() => handleClick('/media/picture')}>
              <IconPicture size="1.8em" />
              <p className="sidebar_text">Picture</p>
            </div>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/blog'))}>
            <div onClick={() => handleClick('/media/blog')}>
              <IconBlog size="1.8em" />
              <p className="sidebar_text">Blog</p>
            </div>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/chat'))}>
            <div onClick={() => handleClick('/media/chat')}>
              <IconChat size="1.8em" />
              <p className="sidebar_text">Chat</p>
            </div>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
