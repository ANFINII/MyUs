import { UserNotification } from 'types/internal/auth'

export const notificationTypes: Array<keyof UserNotification> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
