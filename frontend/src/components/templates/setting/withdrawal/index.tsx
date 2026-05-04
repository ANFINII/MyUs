import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'

export default function Withdrawal(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/')
  const handleNext = () => router.push('/setting/withdrawal/confirm')

  return (
    <Main metaTitle="退会処理">
      <article className="article_registration">
        <div className="form_account">
          <h1 className="login_h1">退会処理</h1>
          <VStack gap="8">
            <Alert type="error">
              退会するとアカウントが利用できなくなります！
              <br />
              この操作は取り消しできません。
            </Alert>
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="red" size="l" name="退会画面に進む" onClick={handleNext} />
            <Button color="blue" size="l" name="ホーム" onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
