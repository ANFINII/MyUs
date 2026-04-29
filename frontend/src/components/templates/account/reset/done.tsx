import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'

export default function ResetDone(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/account/login')

  return (
    <Main metaTitle="パスワード再設定">
      <article className="article_registration">
        <div className="form_account">
          <h1 className="login_h1">パスワード再設定</h1>
          <p className="fs_14">パスワードの再設定が完了しました!</p>
          <VStack gap="12" className="mv_40">
            <Button color="blue" size="l" name="ログイン" onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
