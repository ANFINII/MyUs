import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { PlaylistCreateOut, PlaylistDetailOut, PlaylistIn, PlaylistList, PlaylistAudioIn, PlaylistUpdateIn } from 'types/internal/playlist'
import { apiPlaylist, apiPlaylistAudio, apiPlaylistAudioDelete, apiPlaylists, apiUserPlaylists } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getPlaylists = async (): Promise<ApiOut<PlaylistList>> => {
  return await apiOut(apiClient('json').get(apiPlaylists))
}

export const getUserPlaylists = async (userUlid: string): Promise<ApiOut<PlaylistList>> => {
  return await apiOut(apiClient('json').get(apiUserPlaylists(userUlid)))
}

export const getPlaylist = async (ulid: string): Promise<ApiOut<PlaylistDetailOut>> => {
  return await apiOut(apiClient('json').get(apiPlaylist(ulid)))
}

export const postPlaylist = async (request: PlaylistIn): Promise<ApiOut<PlaylistCreateOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylists, camelSnake(request)))
}

export const putPlaylist = async (ulid: string, request: PlaylistUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiPlaylist(ulid), camelSnake(request)))
}

export const deletePlaylist = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiPlaylist(ulid)))
}

export const postPlaylistAudio = async (ulid: string, request: PlaylistAudioIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiPlaylistAudio(ulid), camelSnake(request)))
}

export const deletePlaylistAudio = async (ulid: string, audioUlid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiPlaylistAudioDelete(ulid, audioUlid)))
}
