import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getGlobalAdvertises } from 'api/internal/advertise'
import AdvertiseCard from 'components/widgets/Card/Advertise'
import style from './GlobalAdvertise.module.scss'

export default function GlobalAdvertise(): React.JSX.Element {
  const { t } = useTranslation()
  const advertises = useQuery({ queryKey: queryKeys.globalAdvertises, queryFn: () => toQuery(getGlobalAdvertises()) })
  const items = advertises.data?.items ?? []

  if (items.length === 0) return <></>

  return (
    <section className={style.advertise}>
      <h3 className={style.heading}>{t('advertise.global')}</h3>
      <div className={style.list}>
        {items.map((item) => (
          <AdvertiseCard key={item.ulid} item={item} />
        ))}
      </div>
    </section>
  )
}
