import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { PlaylistCreateOut, PlaylistIn, PlaylistList, PlaylistMusicIn } from 'types/internal/playlist'
import { apiPlaylistMusic, apiPlaylists } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getPlaylists = async (): Promise<ApiOut<PlaylistList>> => {
  return await apiOut(apiClient('json').get(apiPlaylists))
}

export const postPlaylist = async (request: PlaylistIn): Promise<ApiOut<PlaylistCreateOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylists, camelSnake(request)))
}

export const postPlaylistMusic = async (ulid: string, request: PlaylistMusicIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylistMusic(ulid), camelSnake(request)))
}
