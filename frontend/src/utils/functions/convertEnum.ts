import { CommentType, Locale } from 'utils/constants/enum'
import { assertUnexpected } from './common'

export const commentTypeNameEnum = (typeName: string) => {
  switch (typeName) {
    case CommentType.Video:
      return CommentType.Video
    case CommentType.Music:
      return CommentType.Music
    case CommentType.Blog:
      return CommentType.Blog
    case CommentType.Comic:
      return CommentType.Comic
    case CommentType.Picture:
      return CommentType.Picture
    default:
      return assertUnexpected(typeName)
  }
}

export const localeEnum = (locale?: string): Locale => (locale === Locale.En ? Locale.En : Locale.Ja)
