import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

export default function PasswordChangeDone(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/profile')

  return (
    <Main title="パスワード変更">
      <article className={style.article_pass}>
        <div className={cx(style.form_account, style.password_done)}>
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
