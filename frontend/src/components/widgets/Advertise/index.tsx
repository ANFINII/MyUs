import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUserAdvertises, postAdvertiseRead } from 'api/internal/advertise'
import cx from 'utils/functions/cx'
import ExImage from 'components/parts/ExImage'
import IconCaret from 'components/parts/Icon/Caret'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Advertise.module.scss'

interface Props {
  userUlid: string
  className?: string
}

export default function Advertise(props: Props): React.JSX.Element {
  const { userUlid, className } = props

  const { t } = useTranslation()
  const advertises = useQuery({ queryKey: queryKeys.userAdvertises(userUlid), queryFn: () => toQuery(getUserAdvertises(userUlid)), enabled: userUlid !== '' })
  const items = advertises.data?.items ?? []

  const handleRead = (ulid: string) => postAdvertiseRead(ulid)

  if (items.length === 0) return <></>

  return (
    <div className={cx(style.advertise, className)}>
      <h2 className={style.heading}>{t('advertise.title')}</h2>
      <section>
        <h3 className={style.sub_heading}>{t('advertise.channel')}</h3>
        <VStack gap="4">
          {items.map((item) => (
            <article key={item.ulid}>
              <a href={item.url} target="_blank" rel="noopener noreferrer" className={style.link} onClick={() => handleRead(item.ulid)}>
                <HStack gap="4">
                  {item.video ? (
                    <video src={item.video} poster={item.image} width="192" height="108" preload="metadata" muted className={style.thumbnail} />
                  ) : (
                    <ExImage src={item.image} width="192" height="108" className={style.thumbnail} />
                  )}
                  <VStack gap="2" className={style.content}>
                    <div title={item.title} className={style.title}>
                      {item.title}
                    </div>
                    <div className={style.font}>
                      <IconCaret size="14" className={style.margin} />
                      {item.read}
                    </div>
                  </VStack>
                </HStack>
              </a>
            </article>
          ))}
        </VStack>
      </section>
    </div>
  )
}
