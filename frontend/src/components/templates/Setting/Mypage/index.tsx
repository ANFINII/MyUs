import { useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/router'
import { Mypage } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/widgets/Table'
import TableRow from 'components/widgets/Table/Row'

interface Props {
  mypage: Mypage
}

export default function MyPage(props: Props) {
  const { mypage } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)

  const handleEdit = () => setIsEdit(!isEdit)

  const handlSubmit = () => {
    router.push('/setting/profile')
  }

  return (
    <Main title="マイページ設定" type="table">
      <LoginRequired isAuth={!!mypage}>
        {isEdit ? (
          <div className="button_group">
            <Button green size="xs" name="登録" type="submit" />
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
                <svg xmlns="http://www.w3.org/2000/svg" width="3.5em" height="3.5em" fill="currentColor" className="bi bi-image" viewBox="0 0 16 16">
                  <path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z" />
                  <path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-12zm12 1a1 1 0 0 1 1 1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 1-1h12z" />
                </svg>
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
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              <form method="POST" action="" data-advertise="{{is_advertise}}" ddata-csrf="{{csrf_token}}">
                {mypage.plan === 'Free' ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-disable" viewBox="0 0 16 16">
                    <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                  </svg>
                ) : mypage.isAdvertise ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-on toggle_mypage" viewBox="0 0 16 16">
                    <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-off toggle_mypage" viewBox="0 0 16 16">
                    <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                  </svg>
                )}
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
            <TableRow isIndent label="料金プラン">
              {mypage.plan}
            </TableRow>
            <TableRow isIndent label="全体広告">
              <form method="POST" action="" data-advertise="{{ mypage.is_advertise }}" data-csrf="{{ csrf_token }}">
                {mypage.plan === 'Free' ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-disable" viewBox="0 0 16 16">
                    <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                  </svg>
                ) : mypage.isAdvertise ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-on toggle_mypage" viewBox="0 0 16 16">
                    <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-off toggle_mypage" viewBox="0 0 16 16">
                    <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                  </svg>
                )}
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
