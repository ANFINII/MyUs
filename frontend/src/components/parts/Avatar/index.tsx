import { useState } from 'react'
import clsx from 'clsx'
import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  src: string
  title?: string
  size: string
  imgSize?: string
  color?: 'white' | 'grey'
  className?: string
}

export default function Avatar(props: Props) {
  const { src, title, size, imgSize, color = 'white', className } = props

  const [isError, setIsError] = useState<boolean>(false)

  const handleError = () => setIsError(true)

  return (
    <>
      {isError || src === '' ? (
        <IconPerson size={size} type="circle" className={clsx(className, color)}/>
      ) : (
        <ExImage src={src} title={title} size={imgSize} className={className} onError={handleError} />
      )}
    </>
  )
}
