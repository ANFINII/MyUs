export enum Fetch {
  Save = '保存しました',
  Create = '作成しました',
  Delete = '削除しました',
}

export enum FetchError {
  Error = 'エラーが発生しました',
  Get = 'データの取得に失敗しました',
  Post = 'データの登録に失敗しました',
  Put = 'データの更新に失敗しました',
  Delete = 'データの削除に失敗しました',
}

export enum GenderType {
  Male = 'Male',
  Female = 'Female',
  Secret = 'Secret',
}

export enum GenderView {
  Male = '男性',
  Female = '女性',
  Secret = '秘密',
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

export enum CommentTypeNo {
  Video = 1,
  Music = 2,
  Blog = 3,
  Comic = 4,
  Picture = 5,
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
