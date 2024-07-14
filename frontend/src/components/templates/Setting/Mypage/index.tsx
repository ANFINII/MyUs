import { useState } from 'react'
import { useRouter } from 'next/router'
import { postMypage } from 'api/user'
import { Mypage } from 'types/internal/auth'
import { isEmpty } from 'utils/constants/common'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPicture from 'components/parts/Icon/Picture'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'

interface Props {
  mypage: Mypage
}

export default function SttingMyPage(props: Props) {
  const { mypage } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [values, setValues] = useState<Mypage>(mypage)

  const reset = () => setValues(mypage)
  const handleEdit = () => setIsEdit(!isEdit)
  const handleEmail = (email: string) => setValues({ ...values, email })
  const handleToggle = (isAdvertise: boolean) => setValues({ ...values, isAdvertise: !isAdvertise })
  const handleTagManagerId = (tagManagerId: string) => setValues({ ...values, tagManagerId })
  const handleContent = (content: string) => setValues({ ...values, content })

  const handleBack = () => {
    reset()
    handleEdit()
  }

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    try {
      const data = await postMypage(values)
      data?.message ? setMessage(data.message) : handleEdit()
      handleEdit()
    } catch (e) {
      setMessage('エラーが発生しました！')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUserPage = () => {
    router.push(`/userpage/${mypage.nickname}`)
  }

  return (
    <Main title="マイページ設定" type="table">
      <LoginRequired isAuth={!isEmpty(mypage)}>
        {isEdit ? (
          <div className="button_group">
            <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
            <Button color="blue" size="s" name="戻る" onClick={handleBack} />
          </div>
        ) : (
          <div className="button_group">
            <Button color="blue" size="s" name="編集" onClick={handleEdit} />
            <Button color="purple" size="s" name="ユーザページ" onClick={handleUserPage} />
          </div>
        )}

        {isEdit ? (
          <Table>
            <TableRow label="バナー画像" className="table_header">
              <label htmlFor="account_image_input" className="update_account_image">
                <IconPicture size="3.5em" />
                <input type="file" accept="image/*" id="account_image_input" className="custom-file-input" />
              </label>
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
              <Textarea className="textarea_margin" value={values.content} onChange={handleContent}>
                {values.content}
              </Textarea>
            </TableRow>
          </Table>
        ) : (
          <Table>
            <TableRow label="バナー画像">
              {values.banner !== '' ? (
                <label htmlFor="account_image_input" className="mypage_image">
                  <LightBox width=" 270" height="56" src={values.banner} title={values.nickname} />
                </label>
              ) : (
                <label htmlFor="account_image_input" className="update_account_image">
                  <IconPicture size="3.5em" />
                </label>
              )}
            </TableRow>
            <TableRow isIndent label="投稿者名">
              {values.nickname}
            </TableRow>
            <TableRow isIndent label="メールアドレス">
              {values.email}
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
              <Toggle isActive={values.isAdvertise} disable />
            </TableRow>
            <TableRow isIndent label="タグID">
              GTM{values.tagManagerId && '-' + values.tagManagerId}
            </TableRow>
            <TableRow isIndent label="概要">
              {values.content}
            </TableRow>
          </Table>
        )}
      </LoginRequired>
    </Main>
  )
}
