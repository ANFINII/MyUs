interface Color {
  blue?: boolean
  green?: boolean
  purple?: boolean
  red?: boolean
  light?: boolean
}

interface Props extends Color {
  name: string
  type?: 'submit' | 'reset' | 'button'
  className?: string
  value?: string
  onClick?: () => void
}

export default function Button(props: Props) {
  const {blue, green, purple, red, light} = props
  const {name, type, className, value, onClick} = props
  return (
    <>
      {blue ?
        <button type={type} value={value} className={`button_base blue ${className}`} onClick={onClick}>{name}</button>
      :purple ?
        <button type={type} value={value} className={`button_base purple ${className}`} onClick={onClick}>{name}</button>
      :red ?
        <button type={type} value={value} className={`button_base red ${className}`} onClick={onClick}>{name}</button>
      :green ?
        <button type={type} value={value} className={`button_base green ${className}`} onClick={onClick}>{name}</button>
      :light ?
        <button type={type} value={value} className={`button_base light ${className}`} onClick={onClick}>{name}</button>
      :
        <button type={type} value={value} className={`button_base ${className}`} onClick={onClick}>{name}</button>
      }
    </>
  )
 }
