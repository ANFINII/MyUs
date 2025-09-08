import { useState } from 'react'
import clsx from 'clsx'

interface Props {
  src?: string
  alt?: string
  title?: string
  name?: string
  width?: string
  height?: string
  size?: string
  className?: string
  onClick?: React.MouseEventHandler
  onError?: React.ReactEventHandler
}

export default function ExImage(props: Props): React.JSX.Element {
  const { src, width, height, size, className } = props

  const [imageSrc, setImageSrc] = useState(src)

  const handleError = () => setImageSrc(undefined)
  if (!imageSrc) return <img src="/image/no_image.png" width={width || size} height={height || size} className={className} />

  return <img {...props} width={width || size} height={height || size} className={clsx('cursor_p', className)} onError={handleError} />
}
