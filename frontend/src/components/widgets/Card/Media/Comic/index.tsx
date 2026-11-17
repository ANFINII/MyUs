import { Comic } from 'types/internal/media/output'
import ImageCard from '../Image'

interface Props {
  item: Comic
}

export default function ComicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return <ImageCard href={`/media/comic/${ulid}`} image={image} media={item} />
}
