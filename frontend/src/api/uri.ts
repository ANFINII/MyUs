const base = '/api'

// Auth
export const apiRefresh = base + '/auth/refresh'
export const apiSignup = base + '/auth/signup'
export const apiSignupEmail = base + '/auth/signup/email'
export const apiSignupVerify = base + '/auth/signup/verify'
export const apiLogin = base + '/auth/login'
export const apiLogout = base + '/auth/logout'
export const apiPasswordChange = base + '/auth/password/change'
export const apiPasswordReset = base + '/auth/password/reset'
export const apiPasswordResetEmail = base + '/auth/password/reset/email'
export const apiPasswordResetVerify = base + '/auth/password/reset/verify'
export const apiWithdrawal = base + '/auth/withdrawal'

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
export const apiUserPlaylists = (ulid: string) => base + `/media/playlist/user/${ulid}`
export const apiUserPageAdvertise = (ulid: string) => base + `/user/userpage/${ulid}/advertise`

// Setting
export const apiSettingProfile = base + '/setting/profile'
export const apiSettingMypage = base + '/setting/mypage'
export const apiSettingNotification = base + '/setting/notification'

// Payment
export const apiPaymentSubscription = base + '/payment/subscription'
export const apiPaymentPlans = base + '/payment/plans'
export const apiPaymentCheckout = base + '/payment/checkout'
export const apiPaymentCheckoutProduct = base + '/payment/checkout/product'
export const apiPaymentCancel = base + '/payment/cancel'
export const apiPaymentCancelRevoke = base + '/payment/cancel/revoke'
export const apiPaymentChange = base + '/payment/change'
export const apiPaymentMethod = base + '/payment/method'
export const apiPaymentSeller = base + '/payment/seller'
export const apiPaymentSellerOnboard = base + '/payment/seller/onboard'

// Channel
export const apiChannelCreate = base + '/channel'
export const apiChannelUser = base + '/channel/user'
export const apiChannelSubscribe = base + '/channel/subscribe'
export const apiChannel = (ulid: string) => base + `/channel/${ulid}`
export const apiChannelSeries = (ulid: string) => base + `/media/series/channel/${ulid}`

// Media
export const apiHome = base + '/media/home'

export const apiVideos = base + '/media/video'
export const apiVideo = (ulid: string) => base + `/media/video/${ulid}`

export const apiMusics = base + '/media/music'
export const apiMusic = (ulid: string) => base + `/media/music/${ulid}`
export const apiMusicHires = (ulid: string) => base + `/media/music/${ulid}/hires`

export const apiBlogs = base + '/media/blog'
export const apiBlog = (ulid: string) => base + `/media/blog/${ulid}`

export const apiComics = base + '/media/comic'
export const apiComic = (ulid: string) => base + `/media/comic/${ulid}`

export const apiPictures = base + '/media/picture'
export const apiPicture = (ulid: string) => base + `/media/picture/${ulid}`

export const apiChats = base + '/media/chat'
export const apiChat = (ulid: string) => base + `/media/chat/${ulid}`

export const apiMediaRead = base + '/media/read'
export const apiMediaCategory = base + '/media/category'
export const apiMediaHashtag = base + '/media/hashtag'

export const apiComments = base + '/media/comment'
export const apiComment = (ulid: string) => base + `/media/comment/${ulid}`

export const apiMessages = base + '/media/message'
export const apiMessage = (ulid: string) => base + `/media/message/${ulid}`

export const apiPlaylists = base + '/media/playlist'
export const apiPlaylist = (ulid: string) => base + `/media/playlist/${ulid}`
export const apiPlaylistMusic = (ulid: string) => base + `/media/playlist/${ulid}/music`
export const apiPlaylistMusicDelete = (ulid: string, musicUlid: string) => base + `/media/playlist/${ulid}/music/${musicUlid}`

// Manage
export const apiManageVideos = base + '/manage/media/video'
export const apiManageVideo = (ulid: string) => base + `/manage/media/video/${ulid}`

export const apiManageMusics = base + '/manage/media/music'
export const apiManageMusic = (ulid: string) => base + `/manage/media/music/${ulid}`
export const apiManageMusicHires = (ulid: string) => base + `/manage/media/music/${ulid}/hires`

export const apiManageBlogs = base + '/manage/media/blog'
export const apiManageBlog = (ulid: string) => base + `/manage/media/blog/${ulid}`

export const apiManageComics = base + '/manage/media/comic'
export const apiManageComic = (ulid: string) => base + `/manage/media/comic/${ulid}`

export const apiManagePictures = base + '/manage/media/picture'
export const apiManagePicture = (ulid: string) => base + `/manage/media/picture/${ulid}`

export const apiManageChats = base + '/manage/media/chat'
export const apiManageChat = (ulid: string) => base + `/manage/media/chat/${ulid}`

export const apiManageSeriesList = base + '/manage/series'
export const apiManageSeries = (ulid: string) => base + `/manage/series/${ulid}`

export const apiManageAdvertises = base + '/manage/advertise'
export const apiManageAdvertise = (ulid: string) => base + `/manage/advertise/${ulid}`

export const apiAdvertiseGlobal = base + '/advertise/global'
export const apiAdvertiseUser = (ulid: string) => base + `/advertise/user/${ulid}`
export const apiAdvertiseRead = (ulid: string) => base + `/advertise/${ulid}/read`

// 外部API
export const apiAddress = base + '/search'
