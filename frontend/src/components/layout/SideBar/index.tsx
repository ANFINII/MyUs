import { useRouter } from 'next/router'
import clsx from 'clsx'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import style from './SideBar.module.scss'
import SideBarItem from './SideBarItem'

export default function SideBar(): React.JSX.Element {
  const router = useRouter()

  const isActive = (path: string) => String(router.pathname) === path
  const handleRouter = (path: string) => () => router.push(path)

  const sideBarItems = [
    { path: '/media/video', label: 'Video', icon: <IconVideo size="25" /> },
    { path: '/media/music', label: 'Music', icon: <IconMusic size="25" /> },
    { path: '/media/comic', label: 'Comic', icon: <IconComic size="25" /> },
    { path: '/media/picture', label: 'Picture', icon: <IconPicture size="25" /> },
    { path: '/media/blog', label: 'Blog', icon: <IconBlog size="25" /> },
    { path: '/media/chat', label: 'Chat', icon: <IconChat size="25" /> },
  ]

  return (
    <aside className={style.sidebar}>
      <nav>
        <ul>
          {sideBarItems.map((item) => (
            <SideBarItem
              key={item.path}
              label={item.label}
              icon={item.icon}
              className={clsx(style.sidebar_color, isActive(item.path) && style.active)}
              onClick={handleRouter(item.path)}
            />
          ))}
        </ul>
      </nav>
    </aside>
  )
}
