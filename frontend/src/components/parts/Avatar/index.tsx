import cx from 'utils/functions/cx'
import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'
import style from './Avatar.module.scss'

interface Props {
  src: string
  title?: string
  size: string
  color?: 'white' | 'grey'
  className?: string
}

export default function Avatar(props: Props): React.JSX.Element {
  const { src, title, size, color = 'white', className } = props

  return (
    <>
      {src ? (
        <ExImage src={src} title={title} size={size} className={cx(style.avatar, className)} />
      ) : (
        <IconPerson size={size} type="circle" className={cx(style.avatar, color, className)} />
      )}
    </>
  )
}
