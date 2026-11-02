import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import MusicCreate from './view'

export default function MusicCreatePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())

  return <MusicCreate channels={channels} categories={categories} />
}
