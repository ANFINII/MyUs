import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

export default function UserPolicy(): React.JSX.Element {
  return (
    <Main title="利用規約" type="table">
      <article className="article_userpolicy">
        <p>利用規約を読み同意した上で、本サービスを利用するものとする。</p>
        <p>利用規約に違反している者は本サービンの利用停止、またはユーザー削除を通知なく行うものとします。</p>
        <Divide />

        <h2>第1条 ユーザー登録</h2>
        <p>本サービスのユーザー登録は利用規約を読んだ上で、自己責任とします。</p>
        <p>ユーザー登録をした者は、自己責任において、ユーザーIDおよび、メールアドレス、パスワードを適切に管理するものとします。</p>
        <Divide />

        <h2>第2条 著作権</h2>
        <p>著作者の許可なく本サービスにコンテンツをアップロードすることを禁止いたします。</p>
        <p>著作者の許可なくAI含む二次創作などを本サービスにアップロードすることを禁止いたします。</p>
        <p>本サービスにアップロードしたオリジナルコンテンツの著作権は著作者にあります。</p>
        <Divide />

        <h2>第3条 禁止事項</h2>
        <p>法律に触れる行為を禁止します。</p>
        <p>18禁コンテンツのアップロードを禁止します。</p>
        <p>暴力的、残虐的な表現のあるコンテンツのアップロードを禁止します。</p>
        <p>特定個人や非特定多数の人に対する誹謗中傷することを禁止します。</p>
        <p>MyUs内のコンテンツのスクレイピングを禁止します。</p>
      </article>
    </Main>
  )
}
