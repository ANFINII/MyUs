import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/router'
import IconArrowRight from 'components/parts/Icon/ArrowRight'
import IconCredit from 'components/parts/Icon/Credit'
import IconGrid from 'components/parts/Icon/Grid'
import IconPencil from 'components/parts/Icon/Pencil'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  nickname?: string
  isActive?: boolean
  isStaff?: boolean
  isAuth?: boolean
  isOpen: boolean
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export default function DropMenuProfile(props: Props) {
  const { nickname, isActive, isStaff, isAuth, isOpen, setIsOpen } = props

  const router = useRouter()

  const handleClick = (url: string) => {
    router.push(url)
    setIsOpen(false)
  }

  return (
    <>
      <label className="drop_back_cover"></label>
      <label className="drop_open">
        <Image src={isAuth ? '/img/user.image' : '/img/user_icon.png'} title={nickname} width={32} height={32} alt="" />
      </label>

      {isOpen && (
        <nav className={`drop_menu drop_menu_profile ${isOpen && 'active'}`}>
          <ul>
            <li className="drop_menu_list" onClick={() => handleClick('/setting/profile')}>
              <IconPerson size="1.5em" type="circle" className="color_drop_menu_bi" />
              <span>アカウント</span>
            </li>

            <li className="drop_menu_list" onClick={() => handleClick('/setting/mypage')}>
              <IconPerson size="1.5em" type="square" className="color_drop_menu_bi" />
              <span>マイページ</span>
            </li>

            <li className="drop_menu_list" onClick={() => handleClick('/media/todo')}>
              {/* <Link href={isStaff || isActive ? '/' : '/login'} className="icon_link"></Link> */}
              <IconGrid size="1.5em" className="color_drop_menu_bi" />
              <span>投稿管理</span>
            </li>

            <li className="drop_menu_list" onClick={() => handleClick('/media/todo')}>
              <IconPencil size="1.5em" className="color_drop_menu_bi" />
              <span>ToDo</span>
            </li>

            <li className="drop_menu_list" onClick={() => handleClick('/setting/payment')}>
              <IconCredit size="1.5em" className="color_drop_menu_bi" />
              <span>料金プラン</span>
            </li>

            {!isStaff && (
              <li className="drop_menu_list" onClick={() => handleClick('/setting/withdrawal')}>
                <IconPerson size="1.5em" type="cross" className="color_drop_menu_bi" />
                <span>退会処理</span>
              </li>
            )}

            <li className="drop_menu_list" onClick={() => handleClick('/setting/profile')}>
              <Link href={isAuth ? '/logout' : '/login'} className="icon_link"></Link>
              <IconArrowRight size="1.5em" className="color_drop_menu_bi" />
              <span>ログアウト</span>
            </li>
          </ul>
        </nav>
      )}
    </>
  )
}
