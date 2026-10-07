import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import VStack from 'components/parts/Stack/Vertical'
import style from './Advertise.module.scss'

interface Props {
  isChannelAd: boolean
  className?: string
}

export default function Advertise(props: Props): React.JSX.Element {
  const { isChannelAd, className } = props

  const { t } = useTranslation()

  return (
    <div className={cx(style.advertise, className)}>
      <h2 className={style.heading}>{t('advertise.title')}</h2>
      <VStack gap="4">
        <section>
          <article className={style.article}>{/* 一般広告 */}</article>
        </section>
        {isChannelAd && (
          <section>
            <h3 className={style.sub_heading}>{t('advertise.channel')}</h3>
            <article className={style.article}>{/* チャンネルオーナーの広告 */}</article>
          </section>
        )}
      </VStack>
    </div>
  )
}
