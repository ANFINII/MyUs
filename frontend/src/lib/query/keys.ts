import { AdvertiseSearchParams } from 'types/internal/advertise'
import { SearchParams } from 'types/internal/media/output'

// invalidateQueries で前方一致させるため、配列の先頭から粒度が細かくなるように定義する
export const queryKeys = {
  user: ['user'] as const,
  channels: ['channels'] as const,
  manageVideos: ['manage', 'video'] as const,
  manageVideoList: (params: SearchParams) => ['manage', 'video', params] as const,
  manageMusics: ['manage', 'music'] as const,
  manageMusicList: (params: SearchParams) => ['manage', 'music', params] as const,
  manageBlogs: ['manage', 'blog'] as const,
  manageBlogList: (params: SearchParams) => ['manage', 'blog', params] as const,
  manageComics: ['manage', 'comic'] as const,
  manageComicList: (params: SearchParams) => ['manage', 'comic', params] as const,
  managePictures: ['manage', 'picture'] as const,
  managePictureList: (params: SearchParams) => ['manage', 'picture', params] as const,
  manageChats: ['manage', 'chat'] as const,
  manageChatList: (params: SearchParams) => ['manage', 'chat', params] as const,
  manageAdvertises: ['manage', 'advertise'] as const,
  manageAdvertiseList: (params: AdvertiseSearchParams) => ['manage', 'advertise', params] as const,
}
