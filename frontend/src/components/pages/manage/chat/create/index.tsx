import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import ChatCreate from './view'

export default function ChatCreatePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())

  return <ChatCreate channels={channels} categories={categories} />
}
