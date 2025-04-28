import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { ProfileIn, ProfileOut } from 'types/internal/auth'
import { getAddress } from 'api/external/address'
import { putSettingProfile } from 'api/internal/setting'
import { prefectures } from 'utils/constants/address'
import { selectDate } from 'utils/functions/datetime'
import { genders } from 'utils/functions/user'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Image'
import Radio from 'components/parts/Input/Radio'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import Horizontal from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  profile: ProfileOut
}

export default function SettingProfileEdit(props: Props): JSX.Element {
  const { profile } = props

  const router = useRouter()
  const { updateUser } = useUser()
  const { toast, handleToast } = useToast()
  const { isRequired, isRequiredCheck } = useRequired()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [avatar, setAvatar] = useState<File>()
  const [values, setValues] = useState<ProfileOut>(profile)

  const { years, months, days } = selectDate()
  const handleBack = () => router.push('/setting/profile')
  const handleAvatar = (files: File | File[]) => Array.isArray(files) || setAvatar(files)
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleAutoAddress = async () => {
    const ret = await getAddress(values.postalCode)
    if (ret.isErr()) return handleToast('住所が取得できませんでした!', true)
    const results = ret.value.results
    if (results && results[0]) {
      const result = results[0]
      setValues({ ...values, prefecture: result.address1, city: result.address2, street: result.address3 })
      setMessage('')
    } else {
      setMessage('住所が取得できませんでした!')
    }
  }

  const handlSubmit = async () => {
    const { email, username, nickname, lastName, firstName, phone, postalCode } = values
    if (!isRequiredCheck({ email, username, nickname, lastName, firstName, phone, postalCode })) return
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 200))
    const request: ProfileIn = { ...values, avatar }
    const ret = await putSettingProfile(request)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast('エラーが発生しました！', true)
      return
    }
    const data = ret.value
    if (data.error) {
      setMessage(data.message)
    } else {
      await updateUser()
      handleBack()
    }
    setIsLoading(false)
  }

  const button = (
    <Horizontal gap="4">
      <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
      <Button color="blue" size="s" name="戻る" onClick={handleBack} />
    </Horizontal>
  )

  return (
    <Main title="アカウント設定" type="table" toast={toast} button={button}>
      <LoginError>
        {message && (
          <ul className="messages_profile">
            <li>{message}</li>
          </ul>
        )}

        <Table>
          <TableRow label="アバター画像">
            <InputImage id="avatar" className="account_image_edit" icon={<IconPerson size="56" type="square" />} onChange={handleAvatar} />
          </TableRow>
          <TableRow label="メールアドレス">
            <Input name="email" value={values.email} maxLength={120} required={isRequired} onChange={handleInput} />
          </TableRow>
          <TableRow label="ユーザー名">
            <Input name="username" value={values.username} maxLength={30} placeholder="英数字" required={isRequired} onChange={handleInput} />
          </TableRow>
          <TableRow label="投稿者名">
            <Input name="nickname" value={values.nickname} maxLength={60} required={isRequired} onChange={handleInput} />
          </TableRow>
          <TableRow label="名前">
            <Horizontal gap="1" full>
              <Input name="lastName" value={values.lastName} placeholder="姓" maxLength={30} required={isRequired} onChange={handleInput} />
              <Input name="firstName" value={values.firstName} placeholder="名" maxLength={30} required={isRequired} onChange={handleInput} />
            </Horizontal>
          </TableRow>
          <TableRow label="生年月日">
            <Horizontal gap="1" full>
              <Select name="year" value={values.year} options={years} onChange={handleSelect} />
              <Select name="month" value={values.month} options={months} onChange={handleSelect} />
              <Select name="day" value={values.day} options={days} onChange={handleSelect} />
            </Horizontal>
          </TableRow>
          <TableRow isIndent label="年齢">
            {values.age}歳
          </TableRow>
          <TableRow label="性別">
            <Horizontal gap="5" className="pl_4">
              {genders.map((gender) => (
                <Radio key={gender.key} label={gender.key} name="gender" value={gender.value} checked={gender.value === values.gender} onChange={handleInput} />
              ))}
            </Horizontal>
          </TableRow>
          <TableRow label="電話番号">
            <Input type="tel" name="phone" value={values.phone} maxLength={15} required={isRequired} onChange={handleInput} />
          </TableRow>
          <TableRow label="郵便番号">
            <div className="d_flex">
              <Input type="tel" name="postalCode" value={values.postalCode} maxLength={8} className="mr_2" required={isRequired} onChange={handleInput} />
              <Button name="住所自動入力" onClick={handleAutoAddress} />
            </div>
          </TableRow>
          <TableRow label="住所">
            <Horizontal gap="1" full>
              <Select name="prefecture" value={values.prefecture} options={prefectures} placeholder="都道府県" onChange={handleSelect} />
              <Input name="city" value={values.city} placeholder="市区町村" maxLength={255} onChange={handleInput} />
              <Input name="street" value={values.street} placeholder="町名番地" maxLength={255} onChange={handleInput} />
            </Horizontal>
          </TableRow>
          <TableRow label="自己紹介">
            <Textarea name="introduction" className="textarea_margin" defaultValue={values.introduction} onChange={handleText} />
          </TableRow>
        </Table>
      </LoginError>
    </Main>
  )
}
