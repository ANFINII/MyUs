import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { StaticPath } from 'lib/router'
import Main from 'components/layout/Main'
import IconAdvertise from 'components/parts/Icon/Advertise'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import style from './Manage.module.scss'

const menus: { label: string; icon: React.ReactNode; path: StaticPath }[] = [
  { label: 'Video', icon: <IconVideo size="2em" />, path: '/manage/video' },
  { label: 'Music', icon: <IconMusic size="2em" />, path: '/manage/music' },
  { label: 'Blog', icon: <IconBlog size="2em" />, path: '/manage/blog' },
  { label: 'Comic', icon: <IconComic size="2em" />, path: '/manage/comic' },
  { label: 'Picture', icon: <IconPicture size="2em" />, path: '/manage/picture' },
  { label: 'Chat', icon: <IconChat size="2em" />, path: '/manage/chat' },
  { label: 'Advertise', icon: <IconAdvertise size="2em" />, path: '/manage/advertise' },
]

export default function Manage(): React.JSX.Element {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <Main title={t('manage.title')} type="table" isFooter={false}>
      <div className={style.grid}>
        {menus.map((menu) => (
          <button key={menu.label} type="button" className={style.card} onClick={() => navigate({ to: menu.path })}>
            <div className={style.icon}>{menu.icon}</div>
            <span className={style.label}>{menu.label}</span>
          </button>
        ))}
      </div>
    </Main>
  )
}
