import style from './CurrentBanner.module.scss'

interface Props {
  planName: string
}

export default function CurrentBanner(props: Props): React.JSX.Element {
  const { planName } = props

  return (
    <div className={style.current}>
      <span className={style.label}>現在のプラン</span>
      <span className={style.plan}>{planName}</span>
    </div>
  )
}
