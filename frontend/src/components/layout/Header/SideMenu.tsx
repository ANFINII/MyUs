import { useRouter } from 'next/router'
import clsx from 'clsx'
import { nowDate } from 'utils/functions/datetime'
import ExImage from 'components/parts/ExImage'
import IconArrow from 'components/parts/Icon/Arrow'
import IconFile from 'components/parts/Icon/File'
import IconGlobe from 'components/parts/Icon/Globe'
import IconHouse from 'components/parts/Icon/House'
import IconLightning from 'components/parts/Icon/Lightning'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  open: boolean
  onClose: () => void
}

export default function SideMenu(props: Props) {
  const { open, onClose } = props

  const router = useRouter()

  const handleClick = (url: string) => {
    onClose()
    router.push(url)
  }

  return (
    <aside className={clsx('side_menu', open ? 'active' : '')}>
      <nav>
        <div className="side_menu_close side_menu_color" onClick={onClose}>
          <IconArrow size="1.5em" type="left" className="side_menu_color_bi" />
          <ExImage src="/image/MyUs.png" size="30" />
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
            <ExImage src="/image/MyUs.png" size="24" className="myus_img" />
            <span className="side_menu_footer_item">© {nowDate.year} MyUs Co.,Ltd</span>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
