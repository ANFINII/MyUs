import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { MediaHome } from 'types/internal/media/output'
import { HomeSort } from 'utils/constants/enum'
import { mediaCount } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import SelectBox from 'components/parts/Input/SelectBox'
import MediaIndexList from 'components/widgets/Card/MediaIndexList'

interface Props {
  title: string
  data: MediaHome
  sort: HomeSort
}

export default function Homes(props: Props): React.JSX.Element {
  const { title, data, sort } = props

  const router = useRouter()
  const { t } = useTranslation()
  const search = useSearch(mediaCount(data))

  const sortOptions = Object.values(HomeSort).map((value) => ({ label: t(`homeSort.${value}`), value }))

  const handleSort = (e: ChangeEvent<HTMLSelectElement>) => router.push({ pathname: router.pathname, query: { ...router.query, sort: e.target.value } })

  return (
    <Main title={title} search={search} button={<SelectBox value={sort} options={sortOptions} onChange={handleSort} />}>
      <Divide />
      <MediaIndexList media={data} />
    </Main>
  )
}
