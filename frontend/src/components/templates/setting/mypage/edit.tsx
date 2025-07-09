import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { MypageIn, MypageOut } from 'types/internal/auth'
import { putSettingMypage } from 'api/internal/setting'
import { FetchError } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import IconPicture from 'components/parts/Icon/Picture'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Image'
import Textarea from 'components/parts/Input/Textarea'
import Toggle from 'components/parts/Input/Toggle'
import HStack from 'components/parts/Stack/Horizontal'
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
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleToggle = () => setValues({ ...values, isAdvertise: !values.isAdvertise })

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const request: MypageIn = { ...values, banner }
    const ret = await putSettingMypage(request)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Put, true)
      return
    }
    const data = ret.value
    if (!data.error) handleBack()
    if (data.error) setMessage(data.message)
    setIsLoading(false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
      <Button color="blue" size="s" name="戻る" onClick={handleBack} />
    </HStack>
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
            <Input name="email" value={values.email} maxLength={120} onChange={handleInput} />
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
            {values.plan === 'Free' ? <Toggle isActive={values.isAdvertise} disable /> : <Toggle isActive={values.isAdvertise} onClick={handleToggle} />}
          </TableRow>
          <TableRow label="タグID">
            <Input name="tagManagerId" value={values.tagManagerId} placeholder="タグマネージャーID" maxLength={10} onChange={handleInput} />
          </TableRow>
          <TableRow label="概要">
            <Textarea name="content" defaultValue={values.content} onChange={handleText} />
          </TableRow>
        </Table>
      </LoginError>
    </Main>
  )
}
