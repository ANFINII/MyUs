import { GenderType, GenderView } from 'utils/constants/enum'

export const genderMap: Record<GenderType, GenderView> = {
  [GenderType.Male]: GenderView.Male,
  [GenderType.Female]: GenderView.Female,
  [GenderType.Secret]: GenderView.Secret,
}
