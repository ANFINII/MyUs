import { SearchParams } from 'types/internal/media/output'

// invalidateQueries で前方一致させるため、配列の先頭から粒度が細かくなるように定義する
export const queryKeys = {
  channels: ['channels'] as const,
  manageVideos: ['manage', 'video'] as const,
  manageVideoList: (params: SearchParams) => ['manage', 'video', params] as const,
}
