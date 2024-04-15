interface Props {
  src: string
  alt?: string
  title?: string
  name?: string
  width?: string
  height?: string
  size?: string
  className?: string
}

export default function ExImage(props: Props) {
  const { width, height, size } = props

  return <img {...props} width={width || size} height={height || size} />
}
