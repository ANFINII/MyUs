import clsx from 'clsx'
import style from './ExImage.module.scss'

interface Props {
  src: string
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

export default function ExImage(props: Props) {
  const { width, height, size, className } = props

  return <img {...props} width={width || size} height={height || size} className={clsx(style.image, className)} />
}
