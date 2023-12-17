const base = '/api'

// Auth
export const apiAuth = base + '/auth'
export const apiSignup = base + '/signup'
export const apiLogin = base + '/login'
export const apiLogout = base + '/logout'
export const apiRefresh = base + '/refresh'

// User
export const apiUser = base + '/user'
export const apiProfile = base + '/profile'
export const apiMypage = base + '/mypage'
export const apiNotification = base + '/notification'

// Media
export const apiHome = base + '/home'
export const apiVideos = base + '/media/video'
export const apiVideo = (videoId: number) => base + `/media/video/${videoId}`
export const apiVideoCreate = base + '/media/video/create'

export const apiMusics = base + '/media/music'
export const apiMusic = (musicId: number) => base + `/media/music/${musicId}`
export const apiMusicCreate = base + '/media/music/create'

export const apiPictures = base + '/media/picture'
export const apiPicture = (pictureId: number) => base + `/media/picture/${pictureId}`
export const apiPictureCreate = base + '/media/picture/create'

export const apiBlogs = base + '/media/blog'
export const apiBlog = (blogId: number) => base + `/media/blog/${blogId}`
export const apiBlogCreate = base + '/media/blog/create'

export const apiChats = base + '/media/chat'
export const apiChat = (chatId: number) => base + `/media/chat/${chatId}`
export const apiChatCreate = base + '/media/chat/create'

export const apiTodos = base + '/media/todo'
export const apiTodo = (todoId: number) => base + `/media/todo/${todoId}`
export const apiTodoCreate = base + '/media/todo/create'
