import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'
import InputImage from 'components/parts/Input/Image'
import style from './AvatarInput.module.scss'

interface Props {
  src: string
  onChange: (file: File) => void
}

export default function AvatarInput(props: Props): React.JSX.Element {
  const { src, onChange } = props

  return (
    <InputImage
      id="avatar"
      className={style.input}
      icon={
        src ? (
          <div className={style.image}>
            <ExImage src={src} size="56" />
          </div>
        ) : (
          <IconPerson size="56" type="square" />
        )
      }
      onChange={onChange}
    />
  )
}
