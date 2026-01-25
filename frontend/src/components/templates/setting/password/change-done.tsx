import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'

export default function PasswordChangeDone(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/profile')

  return (
    <Main title="パスワード変更">
      <article className="article_pass">
        <div className="form_account password_done">
          <p className="fs_14">パスワードの変更が完了しました!</p>
          <VStack className="mv_24">
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
