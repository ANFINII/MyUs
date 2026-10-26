export enum Fetch {
  Save = 'fetch.save',
  Delete = 'fetch.delete',
}

export enum FetchError {
  Error = 'fetchError.error',
  Get = 'fetchError.get',
  Post = 'fetchError.post',
  Put = 'fetchError.put',
  Delete = 'fetchError.delete',
}

export enum ErrorType {
  Unauthenticated = 'UNAUTHENTICATED',
  Forbidden = 'FORBIDDEN',
  NotFound = 'NOT_FOUND',
  Validation = 'VALIDATION',
  Internal = 'INTERNAL',
}

export enum GenderType {
  Male = 'Male',
  Female = 'Female',
  Secret = 'Secret',
}

export enum Currency {
  Jpy = 'JPY',
  Usd = 'USD',
  Eur = 'EUR',
  Gbp = 'GBP',
  Cny = 'CNY',
  Krw = 'KRW',
}

export enum Locale {
  Ja = 'Ja',
  En = 'En',
  Zh = 'Zh',
  Ko = 'Ko',
}

export enum MediaType {
  Video = 'Video',
  Music = 'Music',
  Blog = 'Blog',
  Comic = 'Comic',
  Picture = 'Picture',
  Chat = 'Chat',
}

export enum MediaPath {
  Video = 'video',
  Music = 'music',
  Blog = 'blog',
  Comic = 'comic',
  Picture = 'picture',
  Chat = 'chat',
}

export enum NotificationType {
  Video = 'Video',
  Music = 'Music',
  Blog = 'Blog',
  Comic = 'Comic',
  Picture = 'Picture',
  Chat = 'Chat',
  Follow = 'Follow',
  Like = 'Like',
  Reply = 'Reply',
  Views = 'Views',
}

export enum NotificationObjectType {
  Video = 'Video',
  Music = 'Music',
  Blog = 'Blog',
  Comic = 'Comic',
  Picture = 'Picture',
  Chat = 'Chat',
  Follow = 'Follow',
  Comment = 'Comment',
  Message = 'Message',
}

export enum CommentType {
  Video = 'Video',
  Music = 'Music',
  Blog = 'Blog',
  Comic = 'Comic',
  Picture = 'Picture',
}

export enum WsCommand {
  CreateMessage = 'create_message',
  CreateReplyMessage = 'create_reply_message',
  UpdateMessage = 'update_message',
  DeleteMessage = 'delete_message',
}
