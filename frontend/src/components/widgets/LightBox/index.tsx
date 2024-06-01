import { useState } from 'react'
import ExImage from 'components/parts/ExImage'
import IconCross from 'components/parts/Icon/Cross'
import style from './Image.module.scss'

interface Props {
  size: string
  src: string
  title?: string
}

export default function LightBox(props: Props) {
  const { size, src, title } = props

  const [open, setOpen] = useState<boolean>(true)

  const handleToggle = () => setOpen(!open)

  return (
    <>
      <ExImage size={size} src={src} title={title} onClick={handleToggle} />
      <div className={open ? style.light_box : 'd_none'}>
        <div className={style.image_box}>
          <ExImage src={src} title={title} />
          <div className={style.cross}>
            <IconCross size="2em" type="large" onClick={handleToggle} />
          </div>
        </div>
      </div>
    </>
  )
}
