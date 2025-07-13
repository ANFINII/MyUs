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
export const apiFollow = base + '/user/follow'
export const apiFollower = base + '/user/follower'
export const apiNotification = base + '/user/notification'

// Setting
export const apiSettingProfile = base + '/setting/profile'
export const apiSettingMypage = base + '/setting/mypage'
export const apiSettingNotification = base + '/setting/notification'

// Media
export const apiHome = base + '/home'

export const apiVideos = base + '/media/video'
export const apiVideo = (id: number) => base + `/media/video/${id}`
export const apiVideoCreate = base + '/media/video/create'

export const apiMusics = base + '/media/music'
export const apiMusic = (id: number) => base + `/media/music/${id}`
export const apiMusicCreate = base + '/media/music/create'

export const apiComics = base + '/media/comic'
export const apiComic = (id: number) => base + `/media/comic/${id}`
export const apiComicCreate = base + '/media/comic/create'

export const apiPictures = base + '/media/picture'
export const apiPicture = (id: number) => base + `/media/picture/${id}`
export const apiPictureCreate = base + '/media/picture/create'

export const apiBlogs = base + '/media/blog'
export const apiBlog = (id: number) => base + `/media/blog/${id}`
export const apiBlogCreate = base + '/media/blog/create'

export const apiChats = base + '/media/chat'
export const apiChat = (id: number) => base + `/media/chat/${id}`
export const apiChatCreate = base + '/media/chat/create'

export const apiComments = base + '/media/comment'
export const apiComment = (id: number) => base + `/media/comment/${id}`
export const apiCommentLike = base + '/like/form/comment'

// 外部API
export const apiAddress = base + '/search'
