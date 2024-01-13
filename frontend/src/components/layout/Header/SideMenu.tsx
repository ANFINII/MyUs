import Image from 'next/image'
import Link from 'next/link'
import IconArrow from 'components/parts/Icon/Arrow'
import IconFile from 'components/parts/Icon/File'
import IconGlobe from 'components/parts/Icon/Globe'
import IconHouse from 'components/parts/Icon/House'
import IconLightning from 'components/parts/Icon/Lightning'
import IconList from 'components/parts/Icon/List'
import IconPerson from 'components/parts/Icon/Person'

export default function SideMenu() {
  const date = new Date()
  const year = date.getFullYear()

  return (
    <>
      <input type="checkbox" id="burger_menu" className="side_menu" />
      <label htmlFor="burger_menu" className="side_nemu_back"></label>
      <label htmlFor="burger_menu" className="header_color">
        <IconList width="2em" height="1.7em" />
      </label>

      <aside className="side_menu">
        <label htmlFor="burger_menu" className="side_menu_close side_menu_color">
          <IconArrow size="1.5em" type="left" className="side_menu_color_bi" />
          <Image src="/img/MyUs.png" width={30} height={30} alt="" />
        </label>

        <nav>
          <ul>
            <li className="side_menu_item side_menu_color">
              <Link href="/" className="icon_link"></Link>
              <IconHouse size="1.5em" className="side_menu_color_bi" />
              <span>ホーム</span>
            </li>

            <li className="side_menu_item side_menu_color">
              <Link href="/recommend" className="icon_link"></Link>
              <IconLightning size="1.5em" className="side_menu_color_bi" />
              <span>急上昇</span>
            </li>

            <li className="side_menu_item side_menu_color">
              <Link href="/menu/follow" className="icon_link"></Link>
              <IconPerson size="1.5em" type="check" className="side_menu_color_bi" />
              <span>フォロー</span>
            </li>
          </ul>
        </nav>

        <nav className="side_menu_footer">
          <ul>
            <li className="side_menu_item side_menu_color">
              <Link href="/menu/userpolicy" className="icon_link"></Link>
              <IconFile size="1.5em" type="earmark" className="side_menu_color_bi" />
              <span>利用規約</span>
            </li>

            <li className="side_menu_item side_menu_color">
              <Link href="/menu/knowledge" className="icon_link"></Link>
              <IconGlobe size="1.5em" className="side_menu_color_bi" />
              <span>Knowledge Base</span>
            </li>

            <li className="side_menu_footer_item side_menu_color">
              <Link href="/" className="icon_link"></Link>
              <Image src="/img/MyUs.png" width={24} height={24} alt="" className="myus_img" />
              <span className="side_menu_footer_item">© {year} MyUs Co.,Ltd</span>
            </li>
          </ul>
        </nav>
      </aside>
    </>
  )
}
