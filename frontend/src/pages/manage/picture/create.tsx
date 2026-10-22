import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureCreate from 'components/templates/manage/picture/create'

export default function PictureCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <PictureCreate {...props} />}
    </QueryCheck>
  )
}
