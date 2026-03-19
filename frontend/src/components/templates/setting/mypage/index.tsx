import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Option } from 'types/internal/other'
import { MypageOut } from 'types/internal/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import IconPicture from 'components/parts/Icon/Picture'
import SelectBox from 'components/parts/Input/SelectBox'
import Toggle from 'components/parts/Input/Toggle'
import HStack from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'
import style from '../Setting.module.scss'

interface Props {
  mypage: MypageOut
  channels: Channel[]
}

export default function SettingMyPage(props: Props): React.JSX.Element {
  const { mypage, channels } = props

  const router = useRouter()
  const [channelUlid, setChannelUlid] = useState<string>(channels.find((c) => c.isDefault)!.ulid)

  const handleEdit = () => router.push('/setting/mypage/edit')
  const handleUserPage = () => router.push(`/userpage/${mypage.ulid}`)
  const handleSelectChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)

  const channel = channels.find((c) => c.ulid === channelUlid)
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const button = (
    <HStack gap="4">
      <Button color="blue" size="s" name="編集" onClick={handleEdit} />
      <Button color="purple" size="s" name="ユーザページ" onClick={handleUserPage} />
    </HStack>
  )

  return (
    <Main title="マイページ設定" type="table" button={button}>
      <Table>
        <TableRow label="バナー画像">
          {mypage.banner !== '' ? (
            <label htmlFor="account_image" className={style.mypage_image}>
              <LightBox width=" 270" height="56" src={mypage.banner} title={mypage.nickname} />
            </label>
          ) : (
            <label htmlFor="account_image" className={style.account_image_edit}>
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

      <SelectBox value={channelUlid} options={channelOptions} onChange={handleSelectChannel} className={style.channel} />

      <Table>
        {channel && (
          <>
            <TableRow label="アバター">
              {channel.avatar !== '' ? (
                <label className={style.account_image}>
                  <LightBox size="56" src={channel.avatar} title={channel.name} />
                </label>
              ) : (
                <label className={style.account_image_edit}>
                  <IconPerson size="56" type="square" />
                </label>
              )}
            </TableRow>
            <TableRow isIndent label="チャンネル名">
              {channel.name}
            </TableRow>
            <TableRow isIndent label="概要">
              <div className="pv_4 ws_wrap">{channel.description}</div>
            </TableRow>
          </>
        )}
      </Table>
    </Main>
  )
}
