import clsx from 'clsx'
import VStack from 'components/parts/Stack/Vertical'
import style from './Advertise.module.scss'

interface Props {
  isChannelAd: boolean
  className?: string
}

export default function Advertise(props: Props): React.JSX.Element {
  const { isChannelAd, className } = props

  return (
    <div className={clsx(style.advertise, className)}>
      <h2 className={style.heading}>広告表示</h2>
      <VStack gap="4">
        <section>
          <article className={style.article}>{/* 一般広告 */}</article>
        </section>
        {isChannelAd && (
          <section>
            <h3 className={style.sub_heading}>チャンネル広告</h3>
            <article className={style.article}>{/* チャンネルオーナーの広告 */}</article>
          </section>
        )}
      </VStack>
    </div>
  )
}
