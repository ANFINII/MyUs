import { useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/router'
import { Mypage } from 'types/internal/auth'
import { isEmpty } from 'utils/constants/common'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPicture from 'components/parts/Icon/Picture'
import IconToggle from 'components/parts/Icon/Toggle'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
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

  const handleEdit = () => setIsEdit(!isEdit)

  const handlSubmit = () => {
    router.push('/setting/profile')
  }

  return (
    <Main title="マイページ設定" type="table">
      <LoginRequired isAuth={!isEmpty(mypage)}>
        {isEdit ? (
          <div className="button_group">
            <Button green size="xs" name="登録" type="submit" onClick={handlSubmit} />
            <Button blue size="xs" name="戻る" onClick={handleEdit} />
          </div>
        ) : (
          <div className="button_group">
            <Button blue size="xs" name="編集" onClick={handleEdit} />
            <Button purple size="xs" name="ユーザページ" onClick={() => router.push(`/userpage/${mypage.nickname}`)} />
          </div>
        )}

        {isEdit ? (
          <Table>
            <TableRow label="バナー画像" className="table_header">
              <label htmlFor="account_image_input" className="update_account_image">
                <IconPicture size="3.5em" />
                <input type="file" name="banner" accept="image/*" id="account_image_input" className="custom-file-input" />
              </label>
            </TableRow>
            <TableRow isIndent label="投稿者名">
              {mypage.nickname}
            </TableRow>
            <TableRow label="メールアドレス">
              <Input type="text" name="email" value={mypage.email} maxLength={120} className="table_margin" />
            </TableRow>
            <TableRow isIndent label="フォロー数">
              {mypage.followingCount}
            </TableRow>
            <TableRow isIndent label="フォロワー数">
              {mypage.followerCount}
            </TableRow>
            <TableRow label="タグID">
              <Input type="text" name="tag_manager_id" value={mypage.tagManagerId} placeholder="タグマネージャーID" maxLength={10} />
            </TableRow>
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              <form method="POST" action="" data-advertise={mypage.isAdvertise}>
                {mypage.plan === 'Free' ? <IconToggle size="25" type="disable" /> : mypage.isAdvertise ? <IconToggle size="25" type="on" /> : <IconToggle size="25" type="off" />}
              </form>
            </TableRow>
            <TableRow label="概要">
              <Textarea name="introduction" className="textarea_margin">
                {mypage.content}
              </Textarea>
            </TableRow>
          </Table>
        ) : (
          <Table>
            <TableRow label="バナー画像">
              <label htmlFor="account_image_input" className="mypage_image">
                {mypage.banner && (
                  <a href={mypage.banner} data-lightbox="group">
                    <Image src={mypage.banner} title={mypage.nickname} width={270} height={56} alt="" data-lightbox="group" />
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
            <TableRow isIndent label="タグID">
              GTM{mypage.tagManagerId && '-' + mypage.tagManagerId}
            </TableRow>
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              <form method="POST" action="" data-advertise={mypage.isAdvertise}>
                {mypage.plan === 'Free' ? <IconToggle size="25" type="disable" /> : mypage.isAdvertise ? <IconToggle size="25" type="on" /> : <IconToggle size="25" type="off" />}
              </form>
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
