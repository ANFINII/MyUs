interface Props {
  src: string
  alt?: string
  title?: string
  name?: string
  width?: string
  height?: string
  size?: string
  id?: string
  className?: string
}

export default function Image(props: Props) {
  const { width, height, size } = props

  return <img {...props} width={width || size} height={height || size} />
}
