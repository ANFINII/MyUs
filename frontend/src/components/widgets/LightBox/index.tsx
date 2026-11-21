import { useState } from 'react'
import ExImage from 'components/parts/ExImage'
import LightBoxOverlay from './Overlay'

interface Props {
  size?: string
  width?: string
  height?: string
  src: string
  title?: string
}

export default function LightBox(props: Props): React.JSX.Element {
  const { src, title } = props

  const [open, setOpen] = useState<boolean>(false)

  const handleToggle = () => setOpen(!open)
  const handleClose = () => setOpen(false)

  return (
    <>
      <ExImage {...props} onClick={handleToggle} />
      {open && <LightBoxOverlay src={src} title={title} onClose={handleClose} />}
    </>
  )
}
