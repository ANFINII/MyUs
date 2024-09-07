import { useRouter } from 'next/router'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import { nowDate } from 'utils/functions/datetime'
import ExImage from 'components/parts/ExImage'
import IconArrow from 'components/parts/Icon/Arrow'
import IconFile from 'components/parts/Icon/File'
import IconGlobe from 'components/parts/Icon/Globe'
import IconHouse from 'components/parts/Icon/House'
import IconLightning from 'components/parts/Icon/Lightning'
import IconPerson from 'components/parts/Icon/Person'
import SideMenuItem from './Item'

interface Props {
  open: boolean
  onClose: () => void
}

export default function SideMenu(props: Props) {
  const { open, onClose } = props

  const router = useRouter()

  const handleClick = (url: string) => {
    router.push(url)
    onClose()
  }

  return (
    <aside className={clsx('side_menu', isActive(open))}>
      <nav>
        <div className="side_menu_close side_menu_color" onClick={onClose}>
          <IconArrow size="1.5em" type="left" />
          <ExImage src="/image/MyUs.png" size="30" />
        </div>

        <ul>
          <SideMenuItem label="ホーム" icon={<IconHouse size="1.5em" />} onClick={() => handleClick('/')} />
          <SideMenuItem label="急上昇" icon={<IconLightning size="1.5em" type="defalt" />} onClick={() => handleClick('/recommend')} />
          <SideMenuItem label="フォロー" icon={<IconPerson size="1.5em" type="check" />} onClick={() => handleClick('/menu/follow')} />
        </ul>

        <ul className="side_menu_footer">
          <SideMenuItem label="利用規約" icon={<IconFile size="1.5em" type="earmark" />} onClick={() => handleClick('/menu/userpolicy')} />
          <SideMenuItem label="Knowledge Base" icon={<IconGlobe size="1.5em" />} onClick={() => handleClick('/menu/knowledge')} />
          <li className="side_menu_footer_item side_menu_color" onClick={() => handleClick('/')}>
            <ExImage src="/image/MyUs.png" size="24" className="myus_img" />
            <span className="side_menu_footer_item">© {nowDate.year} MyUs Co.,Ltd</span>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
