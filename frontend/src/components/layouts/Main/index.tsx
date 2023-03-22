import {Query} from 'utils/type'
import Meta from 'components/layouts/Head/Meta'

interface Props {
  title?: string
  hero?: string
  query?: Query
  children: React.ReactNode
}

export default function Main(props: Props) {
  const {title, hero, query, children} = props
  return (
    <>
      <Meta title={title} />
      <main className='main'>
        {hero && <h1>{hero}</h1>}
        {query && <section className="search_message">「{query.name}」の検索結果「{query.count}」件</section>}
        {children}
      </main>
    </>
  )
}
