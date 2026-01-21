const base = '/api'

// Auth
export const apiAuth = base + '/auth'
export const apiRefresh = base + '/auth/refresh'
export const apiSignup = base + '/auth/signup'
export const apiLogin = base + '/auth/login'
export const apiLogout = base + '/auth/logout'

// User
export const apiUser = base + '/user/me'
export const apiChannel = base + '/user/channel'
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

// 外部API
export const apiAddress = base + '/search'
