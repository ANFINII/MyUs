import { useState } from 'react'
import { useRouter } from 'next/router'
import { postMypage } from 'api/user'
import { Mypage } from 'types/internal/auth'
import { isEmpty } from 'utils/constants/common'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconPicture from 'components/parts/Icon/Picture'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  mypage: Mypage
}

export default function SttingMyPage(props: Props) {
  const { mypage } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [data, setData] = useState<Mypage>(mypage)

  const handleEdit = () => setIsEdit(!isEdit)
  const handleToggle = (isAdvertise: boolean) => setData((prev) => ({ ...prev, isAdvertise: !isAdvertise }))

  const handlSubmit = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    try {
      const resData = await postMypage(data)
      resData?.message ? setMessage(resData.message) : handleEdit()
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
            <Button color="blue" size="s" name="戻る" onClick={handleEdit} />
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
              {mypage.nickname}
            </TableRow>
            <TableRow label="メールアドレス">
              <Input value={mypage.email} maxLength={120} className="table_margin" />
            </TableRow>
            <TableRow isIndent label="フォロー数">
              {mypage.followingCount}
            </TableRow>
            <TableRow isIndent label="フォロワー数">
              {mypage.followerCount}
            </TableRow>
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              {mypage.plan === 'Free' ? <Toggle isActive={data.isAdvertise} disable /> : <Toggle isActive={data.isAdvertise} onClick={() => handleToggle(data.isAdvertise)} />}
            </TableRow>
            <TableRow label="タグID">
              <Input value={mypage.tagManagerId} placeholder="タグマネージャーID" maxLength={10} />
            </TableRow>
            <TableRow label="概要">
              <Textarea className="textarea_margin">{mypage.content}</Textarea>
            </TableRow>
          </Table>
        ) : (
          <Table>
            <TableRow label="バナー画像">
              <label htmlFor="account_image_input" className="mypage_image">
                {mypage.banner && (
                  <a href={mypage.banner} data-lightbox="group">
                    <ExImage src={mypage.banner} title={mypage.nickname} width="270" height="56" data-lightbox="group" />
                  </a>
                )}
              </label>
            </TableRow>
            <TableRow isIndent label="投稿者名">
              {mypage.nickname}
            </TableRow>
            <TableRow isIndent label="メールアドレス">
              {mypage.email}
            </TableRow>
            <TableRow isIndent label="フォロー数">
              {mypage.followingCount}
            </TableRow>
            <TableRow isIndent label="フォロワー数">
              {mypage.followerCount}
            </TableRow>
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              <Toggle isActive={data.isAdvertise} disable />
            </TableRow>
            <TableRow isIndent label="タグID">
              GTM{mypage.tagManagerId && '-' + mypage.tagManagerId}
            </TableRow>
            <TableRow isIndent label="概要">
              {mypage.content}
            </TableRow>
          </Table>
        )}
      </LoginRequired>
    </Main>
  )
}
