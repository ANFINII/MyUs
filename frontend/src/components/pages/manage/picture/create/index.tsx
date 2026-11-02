import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import PictureCreate from './view'

export default function PictureCreatePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())

  return <PictureCreate channels={channels} categories={categories} />
}
