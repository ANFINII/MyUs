import Divide from 'components/parts/Divide'
import style from './MediaList.module.scss'

interface Props {
  title: string
  divide?: boolean
  children: React.ReactNode
}

export default function MediaIndex(props: Props) {
  const { title, divide = true, children } = props

  return (
    <>
      <article className={style.media_index}>
        <h2>{title}</h2>
        {children}
      </article>
      {divide && <Divide />}
    </>
  )
}
