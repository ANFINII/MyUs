import { UserNotification } from 'types/internal/auth'
import { GenderType, GenderView } from 'utils/constants/enum'

export const genderMap: Record<GenderType, GenderView> = {
  [GenderType.Male]: GenderView.Male,
  [GenderType.Female]: GenderView.Female,
  [GenderType.Secret]: GenderView.Secret,
}

export const notificationTypes: Array<keyof UserNotification> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
