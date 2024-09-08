import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'
import SideBarItem from 'components/parts/NavItem/SideBarItem'

export default function SideBar() {
  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <SideBarItem url="/media/video" label="Video" icon={<IconVideo size="1.8em" />} />
          <SideBarItem url="/media/music" label="Music" icon={<IconMusic size="1.8em" />} />
          <SideBarItem url="/media/comic" label="Comic" icon={<IconComic size="1.8em" />} />
          <SideBarItem url="/media/picture" label="Picture" icon={<IconPicture size="1.8em" />} />
          <SideBarItem url="/media/blog" label="Blog" icon={<IconBlog size="1.8em" />} />
          <SideBarItem url="/media/chat" label="Chat" icon={<IconChat size="1.8em" />} />
        </ul>
      </nav>
    </aside>
  )
}
