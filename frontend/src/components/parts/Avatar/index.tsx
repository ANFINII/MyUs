import { useState } from 'react'
import clsx from 'clsx'
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

export default function Avatar(props: Props): JSX.Element {
  const { src, title, size, color = 'white', className } = props

  const [isError, setIsError] = useState<boolean>(false)

  const handleError = () => setIsError(true)

  return (
    <>
      {isError || src === '' ? (
        <IconPerson size={size} type="circle" className={clsx(style.avatar, color, className)} />
      ) : (
        <ExImage src={src} title={title} size={size} className={clsx(style.avatar, className)} onError={handleError} />
      )}
    </>
  )
}
