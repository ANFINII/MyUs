import { useState } from 'react'
import ExImage from '../ExImage'
import IconPerson from '../Icon/Person'

interface Props {
  size: string
  imgSize: string
  src: string
  nickname: string
  className?: string
}

export default function Avatar(props: Props) {
  const { size, src, imgSize, nickname, className } = props

  const [isError, setIsError] = useState<boolean>(false)

  const handleError = () => setIsError(true)

  return <>{isError || src === '' ? <IconPerson size={size} type="circle" /> : <ExImage src={src} title={nickname} size={imgSize} className={className} onError={handleError} />}</>
}
