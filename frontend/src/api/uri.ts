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

// Setting
export const apiSettingProfile = base + '/setting/profile'
export const apiSettingMypage = base + '/setting/mypage'
export const apiSettingNotification = base + '/setting/notification'

// Media
export const apiHome = base + '/home'

export const apiVideos = base + '/media/video'
export const apiVideo = (ulid: string) => base + `/media/video/${ulid}`
export const apiVideoCreate = base + '/media/video/create'

export const apiMusics = base + '/media/music'
export const apiMusic = (ulid: string) => base + `/media/music/${ulid}`
export const apiMusicCreate = base + '/media/music/create'

export const apiComics = base + '/media/comic'
export const apiComic = (ulid: string) => base + `/media/comic/${ulid}`
export const apiComicCreate = base + '/media/comic/create'

export const apiPictures = base + '/media/picture'
export const apiPicture = (ulid: string) => base + `/media/picture/${ulid}`
export const apiPictureCreate = base + '/media/picture/create'

export const apiBlogs = base + '/media/blog'
export const apiBlog = (ulid: string) => base + `/media/blog/${ulid}`
export const apiBlogCreate = base + '/media/blog/create'

export const apiChats = base + '/media/chat'
export const apiChat = (ulid: string) => base + `/media/chat/${ulid}`
export const apiChatCreate = base + '/media/chat/create'

export const apiComments = base + '/media/comment'
export const apiComment = (ulid: string) => base + `/media/comment/${ulid}`

// 外部API
export const apiAddress = base + '/search'
