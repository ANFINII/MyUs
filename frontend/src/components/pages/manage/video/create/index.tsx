import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import VideoCreate from './view'

export default function VideoCreatePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())

  return <VideoCreate channels={channels} categories={categories} />
}
