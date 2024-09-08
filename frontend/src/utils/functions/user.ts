import { NotificationSetting } from 'types/internal/auth'
import { Gender } from 'utils/constants/enum'

export const genderMap = { [Gender.Male]: '男性', [Gender.Female]: '女性', [Gender.Secret]: '秘密' }

export const genders = [
  { key: '男性', value: '0' },
  { key: '女性', value: '1' },
  { key: '秘密', value: '2' },
]

export const notificationTypes: Array<keyof NotificationSetting> = ['isVideo', 'isMusic', 'isComic', 'isPicture', 'isBlog', 'isChat', 'isFollow', 'isReply', 'isLike', 'isViews']
