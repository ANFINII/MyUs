import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
import ExImage from 'components/parts/ExImage'
import IconArrow from 'components/parts/Icon/Arrow'
import IconFile from 'components/parts/Icon/File'
import IconGlobe from 'components/parts/Icon/Globe'
import IconGrid from 'components/parts/Icon/Grid'
import IconHouse from 'components/parts/Icon/House'
import IconLightning from 'components/parts/Icon/Lightning'
import IconPerson from 'components/parts/Icon/Person'
import NavItem from 'components/parts/NavItem'
import MenuItem from 'components/parts/NavItem/MenuItem'
import style from './SideMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

export default function SideMenu(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const router = useRouter()

  const handleClick = (url: string) => () => {
    router.push(url)
    onClose()
  }

  return (
    <aside className={cx(style.side_menu, open && style.active)}>
      <nav>
        <NavItem className={style.close} icon={<IconArrow size="1.5em" type="left" />} onClick={onClose}>
          <ExImage src="/image/MyUs.png" size="30" />
        </NavItem>

        <ul>
          <MenuItem label="ホーム" icon={<IconHouse size="1.5em" />} className={style.item} onClick={handleClick('/')} />
          <MenuItem label="急上昇" icon={<IconLightning size="1.5em" type="defalt" />} className={style.item} onClick={handleClick('/recommend')} />
          <MenuItem label="フォロー" icon={<IconPerson size="1.5em" type="check" />} className={style.item} onClick={handleClick('/menu/follow')} />
          <MenuItem label="チャンネル" icon={<IconGrid size="1.5em" />} className={style.item} onClick={handleClick('/menu/channel')} />
        </ul>

        <ul className={style.footer}>
          <MenuItem label="利用規約" icon={<IconFile size="1.5em" type="earmark" />} className={style.item} onClick={handleClick('/menu/userpolicy')} />
          <MenuItem label="Knowledge Base" icon={<IconGlobe size="1.5em" />} className={style.item} onClick={handleClick('/menu/knowledge')} />
        </ul>
      </nav>
    </aside>
  )
}
