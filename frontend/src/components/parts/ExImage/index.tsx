import { useState } from 'react'
import cx from 'utils/functions/cx'
import style from './ExImage.module.scss'

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
  const { src, width, height, size, className, ...rest } = props

  const [errorSrc, setErrorSrc] = useState<string>()

  const handleError = () => setErrorSrc(src)

  if (!src || src === errorSrc) return <img src="/image/no_image.png" width={width || size} height={height || size} className={className} />

  return <img {...rest} src={src} width={width || size} height={height || size} className={cx(style.image, className)} onError={handleError} />
}
