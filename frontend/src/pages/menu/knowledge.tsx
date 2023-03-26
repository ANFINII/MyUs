import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'

export default function Knowledge() {
  return (
    <Main title="MyUsナレッジ">
      <article className="article_table">
        <h1>Knowledge Base</h1>
        <table className="table">
          <tbody>
            <tr><td className="td_color">MyUs</td><td className="td_indent">MyUsは総合SNS投稿サイトです。是非いろいろなアイディアを投稿して楽しみましょう!</td></tr>
            <tr><td className="td_color">Video</td><td className="td_indent">動画コンテンツを投稿できる機能です。</td></tr>
            <tr><td className="td_color">Music</td><td className="td_indent">音楽、音声、オーディオブックなどを投稿できる機能です。</td></tr>
            <tr><td className="td_color">Picture</td><td className="td_indent">写真、画像、イラストなどが投稿できる機能です。</td></tr>
            <tr><td className="td_color">Blog</td><td className="td_indent">ブログが投稿できる機能です。具体的にはMyUsに投稿したまとめ、漫画、小説を投稿しても面白いかも知れません。</td></tr>
            <tr><td className="td_color">Chat</td><td className="td_indent">世界中の方とお話できる機能です。掲示板のように使用することもできます!</td></tr>
            <tr><td className="td_color">Collabo</td><td className="td_indent">世界中の方とコラボができる機能です。MyUs内でコラボをして創作活動の幅を広げてみましょう!きっと世界が広がります!</td></tr>
            <tr><td className="td_color">ToDo</td><td className="td_indent">ToDoを管理できる機能です。メモ替りに使用する事もできます。</td></tr>
            <tr><td className="td_color">Myページ</td><td className="td_indent">自分のページを充実させてフォロワーを増やしてみましょう。</td></tr>
            <tr><td className="td_color">フォロー</td><td className="td_indent">フォローしている人やフォロワーさんを確認できる機能です。</td></tr>
            <tr><td className="td_color">検索タグ</td><td className="td_indent">良く検索するワードを20件まで表示できます。投稿管理で表示順序を変更できます。</td></tr>
            <tr><td className="td_color">投稿管理</td><td className="td_indent">投稿した作品などを編集、非公開、削除ができます。タグ付けもこちらで出来ます。</td></tr>
          </tbody>
        </table>
        <Footer />
      </article>
    </Main>
  )
}
