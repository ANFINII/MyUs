import IconHand from 'components/parts/Icon/Hand'
import style from './Like.module.scss'

interface Props {
  isLike?: boolean
  disable?: boolean
  totalLike?: number
  onClick?: () => void
}

export default function CountLike(props: Props) {
  const { isLike, disable, totalLike, onClick } = props

  return (
    <div className={style.count}>
      {disable ? (
        <div>
          <IconHand size="16" type="off" className="mr_8" />
        </div>
      ) : (
        <div className={style.icon} onClick={onClick}>
          <IconHand size="16" type={isLike ? 'on' : 'off'} className={isLike ? style.on : style.off} />
        </div>
      )}
      <span>{totalLike || 0}</span>
    </div>
  )
}
