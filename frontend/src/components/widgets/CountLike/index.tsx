import IconHand from 'components/parts/Icon/Hand'
import style from './CountLike.module.scss'

interface Props {
  isLike: boolean
  disable?: boolean
  size?: string
  count: number
  onClick: () => void
}

export default function CountLike(props: Props): React.JSX.Element {
  const { isLike, disable, size = '16', count, onClick } = props

  return (
    <div className={style.count}>
      {disable ? (
        <div>
          <IconHand size={size} type="off" className={style.off} />
        </div>
      ) : (
        <div className={style.icon} onClick={onClick}>
          <IconHand size={size} type={isLike ? 'on' : 'off'} className={isLike ? style.on : style.off} />
        </div>
      )}
      <span>{count}</span>
    </div>
  )
}
