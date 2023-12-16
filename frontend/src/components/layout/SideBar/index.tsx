import Link from 'next/link'
import { useRouter } from 'next/router'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'

export default function SideBar() {
  const router = useRouter()

  const activeCheck = (url: string) => (router.pathname === url ? ' ' + 'active' : '')

  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <li className={'sidebar_color' + activeCheck('/media/video')}>
            <Link href="/media/video" className="pjax_button">
              <IconVideo />
              <p className="sidebar_text">Video</p>
            </Link>
          </li>

          <li className={'sidebar_color' + activeCheck('/media/music')}>
            <Link href="/media/music" className="pjax_button">
              <IconMusic />
              <p className="sidebar_text">Music</p>
            </Link>
          </li>

          <li className={'sidebar_color' + activeCheck('/media/comic')}>
            <Link href="/media/comic" className="pjax_button">
              <IconComic />
              <p className="sidebar_text">Comic</p>
            </Link>
          </li>

          <li className={'sidebar_color' + activeCheck('/media/picture')}>
            <Link href="/media/picture" className="pjax_button">
              <IconPicture />
              <p className="sidebar_text">Picture</p>
            </Link>
          </li>

          <li className={'sidebar_color' + activeCheck('/media/blog')}>
            <Link href="/media/blog" className="pjax_button">
              <IconBlog />
              <p className="sidebar_text">Blog</p>
            </Link>
          </li>

          <li className={'sidebar_color' + activeCheck('/media/chat')}>
            <Link href="/media/chat" className="pjax_button">
              <IconChat />
              <p className="sidebar_text">Chat</p>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
