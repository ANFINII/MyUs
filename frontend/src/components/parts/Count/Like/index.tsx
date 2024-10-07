import IconHand from 'components/parts/Icon/Hand'
import style from './Like.module.scss'

interface Props {
  isLike?: boolean
  disable?: boolean
  totalLike?: number
}

export default function CountLike(props: Props) {
  const { isLike, disable, totalLike } = props

  return (
    <div className={style.like}>
      {disable ? (
        <IconHand size="16" type="off" className={style.off} />
      ) : (
        <IconHand size="16" type={isLike ? 'on' : 'off'} className={isLike ? style.on : style.off} />
      )}
      <span className={style.like_count}>{totalLike || 0}</span>
    </div>
  )
}
