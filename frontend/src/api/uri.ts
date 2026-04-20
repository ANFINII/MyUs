const base = '/api'

// Auth
export const apiAuth = base + '/auth'
export const apiRefresh = base + '/auth/refresh'
export const apiSignup = base + '/auth/signup'
export const apiLogin = base + '/auth/login'
export const apiLogout = base + '/auth/logout'

// User
export const apiUser = base + '/user/me'
export const apiSearchTag = base + '/user/search_tag'
export const apiFollower = base + '/user/follower'
export const apiFollow = base + '/user/follow'
export const apiFollowUser = base + '/user/follow/user'
export const apiLikeMedia = base + '/user/like/media'
export const apiLikeComment = base + '/user/like/comment'
export const apiNotification = base + '/user/notification'
export const apiNotificationConfirmed = base + '/user/notification/confirmed'
export const apiNotificationDeleted = base + '/user/notification/deleted'
export const apiUserPage = (ulid: string) => base + `/user/userpage/${ulid}`
export const apiUserPageMedia = (ulid: string, channelUlid: string) => base + `/user/userpage/${ulid}/media?channel_ulid=${channelUlid}`

// Setting
export const apiSettingProfile = base + '/setting/profile'
export const apiSettingMypage = base + '/setting/mypage'
export const apiSettingNotification = base + '/setting/notification'

// Channel
export const apiChannelCreate = base + '/channel'
export const apiChannelUser = base + '/channel/user'
export const apiChannelSubscribe = base + '/channel/subscribe'
export const apiChannel = (ulid: string) => base + `/channel/${ulid}`

// Media
export const apiHome = base + '/media/home'
export const apiRecommend = base + '/media/recommend'

export const apiVideos = base + '/media/video'
export const apiVideo = (ulid: string) => base + `/media/video/${ulid}`

export const apiMusics = base + '/media/music'
export const apiMusic = (ulid: string) => base + `/media/music/${ulid}`

export const apiComics = base + '/media/comic'
export const apiComic = (ulid: string) => base + `/media/comic/${ulid}`

export const apiPictures = base + '/media/picture'
export const apiPicture = (ulid: string) => base + `/media/picture/${ulid}`

export const apiBlogs = base + '/media/blog'
export const apiBlog = (ulid: string) => base + `/media/blog/${ulid}`

export const apiChats = base + '/media/chat'
export const apiChat = (ulid: string) => base + `/media/chat/${ulid}`

export const apiComments = base + '/media/comment'
export const apiComment = (ulid: string) => base + `/media/comment/${ulid}`

export const apiMessages = base + '/media/message'
export const apiMessage = (ulid: string) => base + `/media/message/${ulid}`

// Manage
export const apiManageVideos = base + '/manage/media/video'
export const apiManageVideo = (ulid: string) => base + `/manage/media/video/${ulid}`

export const apiManageMusics = base + '/manage/media/music'
export const apiManageMusic = (ulid: string) => base + `/manage/media/music/${ulid}`

export const apiManageComics = base + '/manage/media/comic'
export const apiManageComic = (ulid: string) => base + `/manage/media/comic/${ulid}`

export const apiManagePictures = base + '/manage/media/picture'
export const apiManagePicture = (ulid: string) => base + `/manage/media/picture/${ulid}`

export const apiManageBlogs = base + '/manage/media/blog'
export const apiManageBlog = (ulid: string) => base + `/manage/media/blog/${ulid}`

export const apiManageChats = base + '/manage/media/chat'
export const apiManageChat = (ulid: string) => base + `/manage/media/chat/${ulid}`

// 外部API
export const apiAddress = base + '/search'
