import { AdvertiseSearchParams } from 'types/internal/advertise'
import { SearchParams } from 'types/internal/media/output'

// invalidateQueries で前方一致させるため、配列の先頭から粒度が細かくなるように定義する
export const queryKeys = {
  channels: ['channels'] as const,
  categories: ['categories'] as const,
  manageVideos: ['manage', 'video'] as const,
  manageVideoDetail: (ulid: string) => ['manage', 'video', ulid] as const,
  manageVideoList: (params: SearchParams) => ['manage', 'video', params] as const,
  manageMusics: ['manage', 'music'] as const,
  manageMusicDetail: (ulid: string) => ['manage', 'music', ulid] as const,
  manageMusicList: (params: SearchParams) => ['manage', 'music', params] as const,
  manageBlogs: ['manage', 'blog'] as const,
  manageBlogDetail: (ulid: string) => ['manage', 'blog', ulid] as const,
  manageBlogList: (params: SearchParams) => ['manage', 'blog', params] as const,
  manageComics: ['manage', 'comic'] as const,
  manageComicDetail: (ulid: string) => ['manage', 'comic', ulid] as const,
  manageComicList: (params: SearchParams) => ['manage', 'comic', params] as const,
  managePictures: ['manage', 'picture'] as const,
  managePictureDetail: (ulid: string) => ['manage', 'picture', ulid] as const,
  managePictureList: (params: SearchParams) => ['manage', 'picture', params] as const,
  manageChats: ['manage', 'chat'] as const,
  manageChatDetail: (ulid: string) => ['manage', 'chat', ulid] as const,
  manageChatList: (params: SearchParams) => ['manage', 'chat', params] as const,
  manageAdvertises: ['manage', 'advertise'] as const,
  manageAdvertiseDetail: (ulid: string) => ['manage', 'advertise', ulid] as const,
  manageAdvertiseList: (params: AdvertiseSearchParams) => ['manage', 'advertise', params] as const,
}
