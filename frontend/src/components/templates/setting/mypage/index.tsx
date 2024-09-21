import { useRouter } from 'next/router'
import { MypageOut } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPicture from 'components/parts/Icon/Picture'
import Toggle from 'components/parts/Input/Toggle'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'

interface Props {
  mypage: MypageOut
}

export default function SettingMyPage(props: Props) {
  const { mypage } = props

  const router = useRouter()
  const handleEdit = () => router.push('/setting/mypage/edit')
  const handleUserPage = () => router.push(`/userpage/${mypage.nickname}`)

  const buttonArea = (
    <>
      <Button color="blue" size="s" name="編集" onClick={handleEdit} />
      <Button color="purple" size="s" name="ユーザページ" onClick={handleUserPage} />
    </>
  )

  return (
    <Main title="マイページ設定" type="table" buttonArea={buttonArea}>
      <LoginRequired>
        <Table>
          <TableRow label="バナー画像">
            {mypage.banner !== '' ? (
              <label htmlFor="account_image" className="mypage_image">
                <LightBox width=" 270" height="56" src={mypage.banner} title={mypage.nickname} />
              </label>
            ) : (
              <label htmlFor="account_image" className="account_image_edit">
                <IconPicture size="56" />
              </label>
            )}
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
            <Toggle isActive={mypage.isAdvertise} disable />
          </TableRow>
          <TableRow isIndent label="タグID">
            GTM{mypage.tagManagerId && '-' + mypage.tagManagerId}
          </TableRow>
          <TableRow isIndent label="概要">
            <div className="pv_4 ws_wrap">{mypage.content}</div>
          </TableRow>
        </Table>
      </LoginRequired>
    </Main>
  )
}
