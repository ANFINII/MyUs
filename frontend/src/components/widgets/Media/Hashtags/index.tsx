import { useRouter } from 'next/router'
import { Hashtag } from 'types/internal/media/detail'
import { MediaPath } from 'utils/constants/enum'
import HStack from 'components/parts/Stack/Horizontal'
import style from './Hashtags.module.scss'

interface Props {
  hashtags: Hashtag[]
  mediaPath: MediaPath
}

export default function Hashtags(props: Props): React.JSX.Element {
  const { hashtags, mediaPath } = props
  const router = useRouter()

  const handleRouter = (jpName: string) => {
    router.push(`/media/${mediaPath}?search=${jpName}`)
  }

  return (
    <HStack gap="4" wrap>
      {hashtags.map((hashtag) => (
        <span key={hashtag.jpName} className={style.hashtag} onClick={() => handleRouter(hashtag.jpName)}>
          #{hashtag.jpName}
        </span>
      ))}
    </HStack>
  )
}
