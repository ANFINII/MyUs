import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getGlobalAdvertises, getUserAdvertises } from 'api/internal/advertise'
import cx from 'utils/functions/cx'
import VStack from 'components/parts/Stack/Vertical'
import AdvertiseCard from 'components/widgets/Card/Advertise'
import style from './Advertise.module.scss'

interface Props {
  userUlid: string
  className?: string
}

export default function Advertise(props: Props): React.JSX.Element {
  const { userUlid, className } = props

  const { t } = useTranslation()
  const advertises = useQuery({ queryKey: queryKeys.userAdvertises(userUlid), queryFn: () => toQuery(getUserAdvertises(userUlid)), enabled: userUlid !== '' })
  const globalAdvertises = useQuery({ queryKey: queryKeys.globalAdvertises, queryFn: () => toQuery(getGlobalAdvertises()) })
  const items = advertises.data?.items ?? []
  const globalItems = globalAdvertises.data?.items ?? []

  if (items.length === 0 && globalItems.length === 0) return <></>

  return (
    <div className={cx(style.advertise, className)}>
      <h2 className={style.heading}>{t('advertise.title')}</h2>
      <VStack gap="6">
        {items.length > 0 && (
          <section>
            <h3 className={style.sub_heading}>{t('advertise.channel')}</h3>
            <VStack gap="4">
              {items.map((item) => (
                <AdvertiseCard key={item.ulid} item={item} />
              ))}
            </VStack>
          </section>
        )}
        {globalItems.length > 0 && (
          <section>
            <h3 className={style.sub_heading}>{t('advertise.global')}</h3>
            <VStack gap="4">
              {globalItems.map((item) => (
                <AdvertiseCard key={item.ulid} item={item} />
              ))}
            </VStack>
          </section>
        )}
      </VStack>
    </div>
  )
}
