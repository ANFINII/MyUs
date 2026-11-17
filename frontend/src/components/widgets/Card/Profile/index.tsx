import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Profile.module.scss'

interface Props {
  href: string
  avatar: string
  name: string
  counts: string[]
  description: string
}

export default function ProfileCard(props: Props): React.JSX.Element {
  const { href, avatar, name, counts, description } = props

  return (
    <Card className={style.card}>
      <Link href={href} className={style.box}>
        <HStack gap="5">
          <ExImage src={avatar} title={name} className={style.image} />
          <VStack gap="1" className="fs_12">
            <span title={name}>{name}</span>
            {counts.map((count) => (
              <span key={count}>{count}</span>
            ))}
          </VStack>
        </HStack>
        <div title={description} className={style.description}>
          {description}
        </div>
      </Link>
    </Card>
  )
}
