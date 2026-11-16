import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
<<<<<<< HEAD
import { PlaylistCreateOut, PlaylistDetailOut, PlaylistIn, PlaylistList, PlaylistMusicIn, PlaylistUpdateIn } from 'types/internal/playlist'
import { apiPlaylist, apiPlaylistMusic, apiPlaylists } from 'api/uri'
=======
import { PlaylistCreateOut, PlaylistIn, PlaylistList, PlaylistMusicIn } from 'types/internal/playlist'
import { apiPlaylistMusic, apiPlaylists } from 'api/uri'
>>>>>>> origin/main
import { camelSnake } from 'utils/functions/convertCase'

export const getPlaylists = async (): Promise<ApiOut<PlaylistList>> => {
  return await apiOut(apiClient('json').get(apiPlaylists))
}

<<<<<<< HEAD
export const getPlaylist = async (ulid: string): Promise<ApiOut<PlaylistDetailOut>> => {
  return await apiOut(apiClient('json').get(apiPlaylist(ulid)))
}

=======
>>>>>>> origin/main
export const postPlaylist = async (request: PlaylistIn): Promise<ApiOut<PlaylistCreateOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylists, camelSnake(request)))
}

<<<<<<< HEAD
export const putPlaylist = async (ulid: string, request: PlaylistUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiPlaylist(ulid), camelSnake(request)))
}

export const deletePlaylist = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiPlaylist(ulid)))
}

=======
>>>>>>> origin/main
export const postPlaylistMusic = async (ulid: string, request: PlaylistMusicIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylistMusic(ulid), camelSnake(request)))
}
