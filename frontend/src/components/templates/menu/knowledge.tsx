import { Row } from 'types/internal/table'
import Main from 'components/layout/Main'
import TableList from 'components/widgets/Table/List'

export default function Knowledge() {
  const rows: Row[] = [
    { label: 'MyUs', content: 'MyUsは総合SNS投稿サイトです。是非いろいろなアイディアを投稿して楽しみましょう!' },
    { label: 'Video', content: '動画コンテンツを投稿できる機能です。' },
    { label: 'Music', content: '音楽、音声、オーディオブックなどを投稿できる機能です。' },
    { label: 'Comic', content: '漫画を投稿できる機能です。' },
    { label: 'Picture', content: '写真、画像、イラストなどが投稿できる機能です。' },
    { label: 'Blog', content: 'ブログが投稿できる機能です。具体的にはMyUsに投稿したまとめ、漫画、小説を投稿しても面白いかも知れません。' },
    { label: 'Chat', content: '世界中の方とお話できる機能です。掲示板のように使用することもできます。' },
    { label: 'ToDo', content: 'ToDoを管理できる機能です。メモ替りに使用する事もできます。' },
    { label: 'マイページ', content: '自分のページを充実させてフォロワーを増やしてみましょう。' },
    { label: 'フォロー', content: 'フォローしている人やフォロワーさんを確認できる機能です。' },
    { label: '検索タグ', content: '良く検索するワードを20件まで表示できます。投稿管理で表示順序を変更できます。' },
    { label: '投稿管理', content: '投稿した作品などを編集、非公開、削除ができます。タグ付けもこちらで出来ます。' },
  ]

  return (
    <Main title="Knowledge Base" type="table">
      <TableList rows={rows} />
    </Main>
  )
}
