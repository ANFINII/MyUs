import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import { Option } from 'types/internal/other'
import { MypageOut } from 'types/internal/user'
import { useAppRouter } from 'components/hooks/useAppRouter'
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

  const router = useAppRouter()
  const { t } = useTranslation()
  const [channelUlid, setChannelUlid] = useState<string>(channels.find((c) => c.isDefault)!.ulid)

  const handleEdit = () => router.push('/setting/mypage/edit')
  const handleUserPage = () => router.push(`/userpage/${mypage.ulid}`)
  const handleCreateChannel = () => router.push('/setting/mypage/channel/create')
  const handleSelectChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)

  const channel = channels.find((c) => c.ulid === channelUlid)
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const button = (
    <HStack gap="4">
      <Button color="blue" size="s" name={t('setting.button.edit')} onClick={handleEdit} />
      <Button color="purple" size="s" name={t('setting.mypage.userpage')} onClick={handleUserPage} />
    </HStack>
  )

  return (
    <Main title={t('setting.mypage.title')} type="table" button={button}>
      <Table>
        <TableRow label={t('setting.mypage.banner')}>
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
        <TableRow isIndent label={t('setting.mypage.nickname')}>
          {mypage.nickname}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.email')}>
          {mypage.email}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.following')}>
          {mypage.followingCount}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.followers')}>
          {mypage.followerCount}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.plan')}>
          {mypage.plan}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.advertise')}>
          <Toggle isActive={mypage.isAdvertise} disable />
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.tagId')}>
          GTM{mypage.tagManagerId && '-' + mypage.tagManagerId}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.content')}>
          <div className="pv_4 ws_wrap">{mypage.content}</div>
        </TableRow>
      </Table>

      <HStack gap="8" justify="between" className={style.channel_area}>
        <SelectBox value={channelUlid} options={channelOptions} onChange={handleSelectChannel} className={style.channel} />
        <Button color="green" size="s" name={t('setting.mypage.createChannel')} onClick={handleCreateChannel} />
      </HStack>

      <Table>
        {channel && (
          <>
            <TableRow label={t('setting.mypage.avatar')}>
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
            <TableRow isIndent label={t('setting.mypage.channelName')}>
              {channel.name}
            </TableRow>
            <TableRow isIndent label={t('setting.mypage.description')}>
              <div className="pv_4 ws_wrap">{channel.description}</div>
            </TableRow>
          </>
        )}
      </Table>
    </Main>
  )
}
