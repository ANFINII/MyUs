import { useState } from 'react'
import { useRouter } from 'next/router'
import { MypageIn, MypageOut } from 'types/internal/auth'
import { putSettingMypage } from 'api/internal/setting'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import IconPicture from 'components/parts/Icon/Picture'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Image'
import Textarea from 'components/parts/Input/Textarea'
import Toggle from 'components/parts/Input/Toggle'
import Horizontal from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  mypage: MypageOut
}

export default function SettingMyPageEdit(props: Props): JSX.Element {
  const { mypage } = props

  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [banner, setBanner] = useState<File>()
  const [values, setValues] = useState<MypageOut>(mypage)

  const handleBack = () => router.push('/setting/mypage')
  const handleBanner = (files: File | File[]) => Array.isArray(files) || setBanner(files)
  const handleEmail = (email: string) => setValues({ ...values, email })
  const handleToggle = (isAdvertise: boolean) => setValues({ ...values, isAdvertise: !isAdvertise })
  const handleTagManagerId = (tagManagerId: string) => setValues({ ...values, tagManagerId })
  const handleContent = (content: string) => setValues({ ...values, content })

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const request: MypageIn = { ...values, banner }
    try {
      const data = await putSettingMypage(request)
      if (data) setMessage(data.message)
      if (!data?.error) handleBack()
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  const button = (
    <Horizontal gap="4">
      <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
      <Button color="blue" size="s" name="戻る" onClick={handleBack} />
    </Horizontal>
  )

  return (
    <Main title="マイページ設定" type="table" toast={toast} button={button}>
      <LoginError>
        {message && (
          <ul className="messages_profile">
            <li>{message}</li>
          </ul>
        )}

        <Table>
          <TableRow label="バナー画像">
            <InputImage id="banner" className="account_image_edit" icon={<IconPicture size="56" />} onChange={handleBanner} />
          </TableRow>
          <TableRow isIndent label="投稿者名">
            {values.nickname}
          </TableRow>
          <TableRow label="メールアドレス">
            <Input value={values.email} maxLength={120} onChange={handleEmail} />
          </TableRow>
          <TableRow isIndent label="フォロー数">
            {values.followingCount}
          </TableRow>
          <TableRow isIndent label="フォロワー数">
            {values.followerCount}
          </TableRow>
          <TableRow isIndent label="料金プラン">
            {values.plan}
          </TableRow>
          <TableRow isIndent label="全体広告">
            {values.plan === 'Free' ? <Toggle isActive={values.isAdvertise} disable /> : <Toggle isActive={values.isAdvertise} onClick={() => handleToggle(values.isAdvertise)} />}
          </TableRow>
          <TableRow label="タグID">
            <Input value={values.tagManagerId} placeholder="タグマネージャーID" maxLength={10} onChange={handleTagManagerId} />
          </TableRow>
          <TableRow label="概要">
            <Textarea className="textarea_margin" defaultValue={values.content} onChange={handleContent} />
          </TableRow>
        </Table>
      </LoginError>
    </Main>
  )
}
