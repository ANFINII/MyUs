import { Picture } from 'types/internal/media/output'
import ImageCard from '../Image'

interface Props {
  item: Picture
}

export default function PictureCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return <ImageCard href={`/media/picture/${ulid}`} image={image} media={item} />
}
