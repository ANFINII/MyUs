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

  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <li className={'sidebar_color' + (router.pathname === '/video' ? ' ' + 'active' : '')}>
            <Link href="/video" className="pjax_button">
              <IconVideo />
              <p className="sidebar_text">Video</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/music' ? ' ' + 'active' : '')}>
            <Link href="/music" className="pjax_button">
              <IconMusic />
              <p className="sidebar_text">Music</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/comic' ? ' ' + 'active' : '')}>
            <Link href="/comic" className="pjax_button">
              <IconComic />
              <p className="sidebar_text">Comic</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/picture' ? ' ' + 'active' : '')}>
            <Link href="/picture" className="pjax_button">
              <IconPicture />
              <p className="sidebar_text">Picture</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/blog' ? ' ' + 'active' : '')}>
            <Link href="/blog" className="pjax_button">
              <IconBlog />
              <p className="sidebar_text">Blog</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/chat' ? ' ' + 'active' : '')}>
            <Link href="/chat" className="pjax_button">
              <IconChat />
              <p className="sidebar_text">Chat</p>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
