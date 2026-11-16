import { useSuspenseQuery } from '@tanstack/react-query'
import { playlistsQuery } from 'lib/query/options'
import Playlists from './view'

export default function PlaylistsPage(): React.JSX.Element {
  const { data } = useSuspenseQuery(playlistsQuery())

  return <Playlists data={data} />
}
