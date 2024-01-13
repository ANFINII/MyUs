import Image from 'next/image'
import { useRouter } from 'next/router'
import IconArrow from 'components/parts/Icon/Arrow'
import IconFile from 'components/parts/Icon/File'
import IconGlobe from 'components/parts/Icon/Globe'
import IconHouse from 'components/parts/Icon/House'
import IconLightning from 'components/parts/Icon/Lightning'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  isOpen: boolean
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export default function SideMenu(props: Props) {
  const { isOpen, setIsOpen } = props

  const router = useRouter()

  const date = new Date()
  const handleClose = () => setIsOpen(false)
  const handleClick = (url: string) => {
    router.push(url)
    setIsOpen(false)
  }

  return (
    <aside className={'side_menu' + (isOpen ? ' ' + 'active' : '')}>
      <nav>
        <div className="side_menu_close side_menu_color" onClick={handleClose}>
          <IconArrow size="1.5em" type="left" className="side_menu_color_bi" />
          <Image src="/image/MyUs.png" width={30} height={30} alt="" />
        </div>

        <ul>
          <li className="side_menu_item side_menu_color" onClick={() => handleClick('/')}>
            <IconHouse size="1.5em" className="side_menu_color_bi" />
            <span>ホーム</span>
          </li>

          <li className="side_menu_item side_menu_color" onClick={() => handleClick('/recommend')}>
            <IconLightning size="1.5em" type="defalt" className="side_menu_color_bi" />
            <span>急上昇</span>
          </li>

          <li className="side_menu_item side_menu_color" onClick={() => handleClick('/menu/follow')}>
            <IconPerson size="1.5em" type="check" className="side_menu_color_bi" />
            <span>フォロー</span>
          </li>
        </ul>

        <ul className="side_menu_footer">
          <li className="side_menu_item side_menu_color icon_link" onClick={() => handleClick('/menu/userpolicy')}>
            <IconFile size="1.5em" type="earmark" className="side_menu_color_bi" />
            <span>利用規約</span>
          </li>

          <li className="side_menu_item side_menu_color" onClick={() => handleClick('/menu/knowledge')}>
            <IconGlobe size="1.5em" className="side_menu_color_bi" />
            <span>Knowledge Base</span>
          </li>

          <li className="side_menu_footer_item side_menu_color" onClick={() => handleClick('/')}>
            <Image src="/image/MyUs.png" width={24} height={24} alt="" className="myus_img" />
            <span className="side_menu_footer_item">© {date.getFullYear()} MyUs Co.,Ltd</span>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
