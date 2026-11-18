import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, paymentSellerQuery } from 'lib/query/options'
import BlogCreate from './view'

export default function BlogCreatePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())

  return <BlogCreate channels={channels} categories={categories} seller={seller} />
}
