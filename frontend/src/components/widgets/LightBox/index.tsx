import { useState } from 'react'
import ExImage from 'components/parts/ExImage'
import IconCross from 'components/parts/Icon/Cross'
import style from './LightBox.module.scss'

interface Props {
  size?: string
  width?: string
  height?: string
  src: string
  title?: string
}

export default function LightBox(props: Props) {
  const { src, title } = props

  const [open, setOpen] = useState<boolean>(false)

  const handleToggle = () => setOpen(!open)
  const handleClose = () => setOpen(false)

  return (
    <>
      <ExImage {...props} onClick={handleToggle} />
      <div className={open ? style.light_box : 'd_none'} onClick={handleClose}>
        <div className={style.image_box}>
          <div>
            <ExImage src={src} title={title} />
            <div className={style.cross}>
              <IconCross size="2em" type="large" onClick={handleToggle} />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
