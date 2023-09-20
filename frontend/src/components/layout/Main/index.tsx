import { Search } from 'types/media'

interface Props {
  title?: string
  search?: Search
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, search, children } = props

  return (
    <main className="main">
      {title && <h1>{title}</h1>}
      {search && (
        <section className="search_message">
          「{search.name}」の検索結果「{search.count}」件
        </section>
      )}
      {children}
    </main>
  )
}
