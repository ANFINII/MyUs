import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'
import InputImage from 'components/parts/Input/Image'
import style from '../../Setting.module.scss'

interface Props {
  src: string
  onChange: (file: File) => void
}

export default function AvatarInput(props: Props): React.JSX.Element {
  const { src, onChange } = props

  return (
    <InputImage
      id="avatar"
      className={style.account_image_edit}
      icon={
        src ? (
          <div className={style.account_image}>
            <ExImage src={src} size="56" />
          </div>
        ) : (
          <div className={style.account_image_edit}>
            <IconPerson size="56" type="square" />
          </div>
        )
      }
      onChange={onChange}
    />
  )
}
