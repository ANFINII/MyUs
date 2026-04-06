import { Blog } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import BlogCard from 'components/widgets/Card/Media/Blog'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Blog" search={search}>
      <CardList items={datas} Content={BlogCard} />
    </Main>
  )
}
