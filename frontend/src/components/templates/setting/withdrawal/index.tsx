import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

export default function Withdrawal(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/')
  const handleNext = () => router.push('/setting/withdrawal/confirm')

  return (
    <Main title="退会処理">
      <article className={style.article_pass}>
        <div className={style.form_account}>
          <VStack gap="8" className="ws_nowrap">
            <p>退会するとアカウントが利用できなくなります！</p>
            <p className="red">この操作は取り消しできません。</p>
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
