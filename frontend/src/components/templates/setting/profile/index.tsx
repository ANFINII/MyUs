import { useTranslation } from 'react-i18next'
import { ProfileOut } from 'types/internal/user'
import { getAge, getFullName } from 'utils/functions/user'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import HStack from 'components/parts/Stack/Horizontal'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'
import style from '../Setting.module.scss'

interface Props {
  profile: ProfileOut
}

export default function SettingProfile(props: Props): React.JSX.Element {
  const { profile } = props

  const router = useAppRouter()
  const { t } = useTranslation()
  const handleEdit = () => router.push('/setting/profile/edit')
  const handlePassword = () => router.push('/setting/password/change')

  const button = (
    <HStack gap="4">
      <Button color="blue" size="s" name={t('setting.button.edit')} onClick={handleEdit} />
      <Button color="blue" size="s" name={t('setting.profile.passwordChange')} onClick={handlePassword} />
    </HStack>
  )

  return (
    <Main title={t('setting.profile.title')} type="table" button={button}>
      <Table>
        <TableRow label={t('setting.profile.avatar')}>
          {profile.avatar !== '' ? (
            <label className={style.account_image}>
              <LightBox size="56" src={profile.avatar} title={profile.nickname} />
            </label>
          ) : (
            <label className={style.account_image_edit}>
              <IconPerson size="56" type="square" />
            </label>
          )}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.email')}>
          {profile.email}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.username')}>
          {profile.username}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.nickname')}>
          {profile.nickname}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.name')}>
          {getFullName(profile.lastName, profile.firstName)}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.birthday')}>
          {t('setting.profile.birthdayValue', { year: profile.year, month: profile.month, day: profile.day })}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.age')}>
          {t('setting.profile.ageValue', { count: getAge(profile.year, profile.month, profile.day) })}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.gender')}>
          {t(`gender.${profile.gender}`)}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.phone')}>
          {profile.phone}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.postalCode')}>
          {profile.postalCode}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.address')}>
          {profile.prefecture}
          {profile.city}
          {profile.street}
        </TableRow>
        <TableRow isIndent label={t('setting.profile.introduction')}>
          <div className="pv_4 ws_wrap">{profile.introduction}</div>
        </TableRow>
      </Table>
    </Main>
  )
}
