import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { ChannelIn, Channel } from 'types/internal/channel'
import { Option } from 'types/internal/other'
import { MypageIn, MypageOut } from 'types/internal/user'
import { putChannel } from 'api/internal/channel'
import { putSettingMypage } from 'api/internal/setting'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useLoading } from 'components/hooks/useLoading'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'
import IconPicture from 'components/parts/Icon/Picture'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Image'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import Toggle from 'components/parts/Input/Toggle'
import HStack from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import style from '../Setting.module.scss'

interface Props {
  mypage: MypageOut
  channels: Channel[]
}

export default function SettingMyPageEdit(props: Props): React.JSX.Element {
  const { mypage, channels } = props

  const navigate = useNavigate()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const { message, handleError } = useApiError({ handleToast })
  const [bannerFile, setBannerFile] = useState<File>()
  const [mypageValues, setMypageValues] = useState<MypageOut>(mypage)
  const [avatarFile, setAvatarFile] = useState<File>()
  const [channelUlid, setChannelUlid] = useState<string>(channels.find((c) => c.isDefault)!.ulid)
  const [channelValues, setChannelValues] = useState<Record<string, Channel>>(Object.fromEntries(channels.map((c) => [c.ulid, c])))

  const channel = channelValues[channelUlid]!
  const bannerUrl = bannerFile ? URL.createObjectURL(bannerFile) : mypage.banner
  const avatarUrl = avatarFile ? URL.createObjectURL(avatarFile) : channel.avatar
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const handleBack = () => navigate({ to: '/setting/mypage' })
  const handleBanner = (files: File | File[]) => Array.isArray(files) || setBannerFile(files)
  const handleAvatar = (files: File | File[]) => Array.isArray(files) || setAvatarFile(files)
  const handleToggle = () => setMypageValues({ ...mypageValues, isAdvertise: !mypageValues.isAdvertise })
  const handleMypageInput = (e: ChangeEvent<HTMLInputElement>) => setMypageValues({ ...mypageValues, [e.target.name]: e.target.value })
  const handleMypageText = (e: ChangeEvent<HTMLTextAreaElement>) => setMypageValues({ ...mypageValues, [e.target.name]: e.target.value })

  const handleSelectChannel = (e: ChangeEvent<HTMLSelectElement>) => {
    setChannelUlid(e.target.value)
    setAvatarFile(undefined)
  }

  const handleChannelInput = (e: ChangeEvent<HTMLInputElement>) => {
    setChannelValues({ ...channelValues, [channelUlid]: { ...channel, [e.target.name]: e.target.value } })
  }

  const handleChannelText = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setChannelValues({ ...channelValues, [channelUlid]: { ...channel, [e.target.name]: e.target.value } })
  }

  const handleSubmit = async () => {
    handleLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const request: MypageIn = { ...mypageValues, bannerFile }
    const ret = await putSettingMypage(request)
    if (ret.isErr()) {
      const message = ret.error.message
      handleError(FetchError.Put, message)
      handleLoading(false)
      return
    }

    const channelRequest: ChannelIn = { name: channel.name, description: channel.description, avatarFile }
    const channelRet = await putChannel(channelUlid, channelRequest)
    if (channelRet.isErr()) {
      const message = channelRet.error.message
      handleError(FetchError.Put, message)
      handleLoading(false)
      return
    }
    handleBack()
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('setting.button.register')} loading={loading} onClick={handleSubmit} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title={t('setting.mypage.title')} type="table" toast={toast} button={button}>
      {message && (
        <ul className={style.messages_profile}>
          <li>{message}</li>
        </ul>
      )}

      <Table>
        <TableRow label={t('setting.mypage.banner')}>
          <InputImage
            id="banner"
            className={style.account_image_edit}
            icon={
              bannerUrl ? (
                <div className={style.mypage_image}>
                  <ExImage src={bannerUrl} width="270" height="56" />
                </div>
              ) : (
                <div className={style.account_image_edit}>
                  <IconPicture size="56" />
                </div>
              )
            }
            onChange={handleBanner}
          />
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.nickname')}>
          {mypageValues.nickname}
        </TableRow>
        <TableRow label={t('setting.mypage.email')}>
          <Input name="email" value={mypageValues.email} maxLength={120} onChange={handleMypageInput} />
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.following')}>
          {mypageValues.followingCount}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.followers')}>
          {mypageValues.followerCount}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.plan')}>
          {mypageValues.plan}
        </TableRow>
        <TableRow isIndent label={t('setting.mypage.advertise')}>
          {mypageValues.plan === 'Free' ? <Toggle isActive={mypageValues.isAdvertise} disable /> : <Toggle isActive={mypageValues.isAdvertise} onClick={handleToggle} />}
        </TableRow>
        <TableRow label={t('setting.mypage.tagId')}>
          <Input name="tagManagerId" value={mypageValues.tagManagerId} placeholder={t('setting.mypage.tagIdPlaceholder')} maxLength={10} onChange={handleMypageInput} />
        </TableRow>
        <TableRow label={t('setting.mypage.content')}>
          <Textarea name="content" defaultValue={mypageValues.content} onChange={handleMypageText} />
        </TableRow>
      </Table>

      <SelectBox value={channelUlid} options={channelOptions} onChange={handleSelectChannel} className={style.channel} />

      <Table key={channelUlid}>
        <TableRow label={t('setting.mypage.avatarImage')}>
          <InputImage
            id="avatar"
            className={style.account_image_edit}
            icon={
              avatarUrl ? (
                <div className={style.account_image}>
                  <ExImage src={avatarUrl} size="56" />
                </div>
              ) : (
                <div className={style.account_image_edit}>
                  <IconPerson size="56" type="square" />
                </div>
              )
            }
            onChange={handleAvatar}
          />
        </TableRow>
        <TableRow label={t('setting.mypage.channelName')}>
          <Input name="name" value={channel.name} maxLength={50} onChange={handleChannelInput} />
        </TableRow>
        <TableRow label={t('setting.mypage.description')}>
          <Textarea name="description" defaultValue={channel.description} onChange={handleChannelText} />
        </TableRow>
      </Table>
    </Main>
  )
}
