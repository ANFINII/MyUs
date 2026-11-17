import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import style from './Collection.module.scss'

interface Props {
  href: string
  image: string
  icon?: React.ReactNode
  count: string
  title: string
  sub: string
}

export default function CollectionCard(props: Props): React.JSX.Element {
  const { href, image, icon, count, title, sub } = props

  return (
    <Card className={style.card}>
      <Link href={href} className={style.link}>
        <div className={style.thumbnail_box}>
          {!image && icon ? <span className={style.icon}>{icon}</span> : <ExImage src={image} width="195" height="195" className={style.thumbnail} />}
          <span className={style.count}>{count}</span>
        </div>
        <div className={style.content}>
          <div title={title} className={style.title}>
            {title}
          </div>
          <div className={style.sub}>{sub}</div>
        </div>
      </Link>
    </Card>
  )
}
