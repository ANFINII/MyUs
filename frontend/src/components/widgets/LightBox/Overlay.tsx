import ExImage from 'components/parts/ExImage'
import IconCross from 'components/parts/Icon/Cross'
import style from './LightBox.module.scss'

interface Props {
  src: string
  title?: string
  onClose: () => void
}

export default function LightBoxOverlay(props: Props): React.JSX.Element {
  const { src, title, onClose } = props

  return (
    <div className={style.light_box} onClick={onClose}>
      <div className={style.image_box}>
        <div>
          <ExImage src={src} title={title} onClick={(e) => e.stopPropagation()} />
          <div className={style.cross}>
            <IconCross size="2em" type="large" onClick={onClose} />
          </div>
        </div>
      </div>
    </div>
  )
}
