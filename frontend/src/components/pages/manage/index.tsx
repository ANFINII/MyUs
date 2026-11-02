import { useSuspenseQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import Manage from './view'

export default function ManagePage(): React.JSX.Element {
  useSuspenseQuery(userQuery())

  return <Manage />
}
