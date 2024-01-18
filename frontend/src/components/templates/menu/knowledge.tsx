import Main from 'components/layout/Main'
import Table from 'components/widgets/Table'
import TableRow from 'components/widgets/Table/Row'

export default function Knowledge() {
  return (
    <Main title="Knowledge Base" type="table">
      <Table>
        <TableRow isIndent label="MyUs">
          MyUsは総合SNS投稿サイトです。是非いろいろなアイディアを投稿して楽しみましょう!
        </TableRow>
        <TableRow isIndent label="Video">
          動画コンテンツを投稿できる機能です。
        </TableRow>
        <TableRow isIndent label="Music">
          音楽、音声、オーディオブックなどを投稿できる機能です。
        </TableRow>
        <TableRow isIndent label="Comic">
          漫画を投稿できる機能です。
        </TableRow>
        <TableRow isIndent label="Picture">
          写真、画像、イラストなどが投稿できる機能です。
        </TableRow>
        <TableRow isIndent label="Blog">
          ブログが投稿できる機能です。具体的にはMyUsに投稿したまとめ、漫画、小説を投稿しても面白いかも知れません。
        </TableRow>
        <TableRow isIndent label="Chat">
          世界中の方とお話できる機能です。掲示板のように使用することもできます。
        </TableRow>
        <TableRow isIndent label="ToDo">
          ToDoを管理できる機能です。メモ替りに使用する事もできます。
        </TableRow>
        <TableRow isIndent label="マイページ">
          自分のページを充実させてフォロワーを増やしてみましょう。
        </TableRow>
        <TableRow isIndent label="フォロー">
          フォローしている人やフォロワーさんを確認できる機能です。
        </TableRow>
        <TableRow isIndent label="検索タグ">
          良く検索するワードを20件まで表示できます。投稿管理で表示順序を変更できます。
        </TableRow>
        <TableRow isIndent label="投稿管理">
          投稿した作品などを編集、非公開、削除ができます。タグ付けもこちらで出来ます。
        </TableRow>
      </Table>
    </Main>
  )
}
