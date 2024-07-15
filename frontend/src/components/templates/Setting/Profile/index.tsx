import { useRouter } from 'next/router'
import { ProfileOut } from 'types/internal/auth'
import { isEmpty } from 'utils/constants/common'
import { genderMap } from 'utils/functions/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'

interface Props {
  profile: ProfileOut
}

export default function SettingProfile(props: Props) {
  const { profile } = props

  const router = useRouter()
  const handleEdit = () => router.push('/setting/profile/edit')
  const handlePassword = () => router.push('/setting/password/change')

  return (
    <Main title="アカウント設定" type="table">
      <LoginRequired isAuth={!isEmpty(profile)}>
        <div className="button_group">
          <Button color="blue" size="s" name="編集" onClick={handleEdit} />
          <Button color="blue" size="s" name="パスワード変更" onClick={handlePassword} />
        </div>

        <Table>
          <TableRow label="アカウント画像" className="table_header">
            {profile.avatar !== '' ? (
              <label className="account_image">
                <LightBox size="56" src={profile.avatar} title={profile.nickname} />
              </label>
            ) : (
              <label className="account_image_edit">
                <IconPerson size="3.5em" type="square" />
              </label>
            )}
          </TableRow>
          <TableRow isIndent label="メールアドレス">
            {profile.email}
          </TableRow>
          <TableRow isIndent label="ユーザー名">
            {profile.username}
          </TableRow>
          <TableRow isIndent label="投稿者名">
            {profile.nickname}
          </TableRow>
          <TableRow isIndent label="名前">
            {profile.fullName}
          </TableRow>
          <TableRow isIndent label="生年月日">
            {profile.year}年{profile.month}月{profile.day}日
          </TableRow>
          <TableRow isIndent label="年齢">
            {profile.age}歳
          </TableRow>
          <TableRow isIndent label="性別">
            {genderMap[profile.gender]}
          </TableRow>
          <TableRow isIndent label="電話番号">
            {profile.phone}
          </TableRow>
          <TableRow isIndent label="郵便番号">
            {profile.postalCode}
          </TableRow>
          <TableRow isIndent label="住所">
            {profile.prefecture} {profile.city}
            {profile.street} {profile.building}
          </TableRow>
          <TableRow isIndent label="自己紹介">
            {profile.introduction}
          </TableRow>
        </Table>
      </LoginRequired>
    </Main>
  )
}
