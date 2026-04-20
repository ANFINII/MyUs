import { useRouter } from 'next/router'
import Main from 'components/layout/Main'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import style from './Manage.module.scss'

const menus = [
  { label: 'Video', icon: <IconVideo size="2em" />, path: 'video' },
  { label: 'Music', icon: <IconMusic size="2em" />, path: 'music' },
  { label: 'Blog', icon: <IconBlog size="2em" />, path: 'blog' },
  { label: 'Comic', icon: <IconComic size="2em" />, path: 'comic' },
  { label: 'Picture', icon: <IconPicture size="2em" />, path: 'picture' },
  { label: 'Chat', icon: <IconChat size="2em" />, path: 'chat' },
]

export default function Manage(): React.JSX.Element {
  const router = useRouter()

  return (
    <Main title="投稿管理" type="table" isFooter={false}>
      <div className={style.grid}>
        {menus.map((menu) => (
          <button key={menu.label} type="button" className={style.card} onClick={() => router.push(`/manage/${menu.path}`)}>
            <div className={style.icon}>{menu.icon}</div>
            <span className={style.label}>{menu.label}</span>
          </button>
        ))}
      </div>
    </Main>
  )
}
