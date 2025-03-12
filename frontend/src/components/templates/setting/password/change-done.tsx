import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Vertical from 'components/parts/Stack/Vertical'

export default function PasswordChangeDone(): JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/profile')

  return (
    <Main title="パスワード変更">
      <LoginError>
        <article className="article_pass">
          <div className="form_account password_done">
            <p className="fs_14">パスワードの変更が完了しました!</p>
            <Vertical className='mv_24'>
              <Button color="blue" size="l" name="戻る" onClick={handleBack} />
            </Vertical>
          </div>
        </article>
      </LoginError>
      <Footer />
    </Main>
  )
}
