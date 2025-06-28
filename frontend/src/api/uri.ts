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
export const apiVideo = (videoId: number) => base + `/media/video/${videoId}`
export const apiVideoCreate = base + '/media/video/create'

export const apiMusics = base + '/media/music'
export const apiMusic = (musicId: number) => base + `/media/music/${musicId}`
export const apiMusicCreate = base + '/media/music/create'

export const apiComics = base + '/media/comic'
export const apiComic = (comicId: number) => base + `/media/comic/${comicId}`
export const apiComicCreate = base + '/media/comic/create'

export const apiPictures = base + '/media/picture'
export const apiPicture = (pictureId: number) => base + `/media/picture/${pictureId}`
export const apiPictureCreate = base + '/media/picture/create'

export const apiBlogs = base + '/media/blog'
export const apiBlog = (blogId: number) => base + `/media/blog/${blogId}`
export const apiBlogCreate = base + '/media/blog/create'

export const apiChats = base + '/media/chat'
export const apiChat = (chatId: number) => base + `/media/chat/${chatId}`
export const apiChatCreate = base + '/media/chat/create'

export const apiCommnet = (id: number) => base + `/media/${id}/comment`
export const apiCommentLike = base + '/like/form/comment'

// 外部API
export const apiAddress = base + '/search'
