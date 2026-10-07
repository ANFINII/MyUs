import { useTranslation } from 'react-i18next'
import Button from 'components/parts/Button'

interface Props {
  isFollow: boolean
  disabled: boolean
  onClick: () => void
}

export default function FollowButton(props: Props): React.JSX.Element {
  const { isFollow, disabled, onClick } = props

  const { t } = useTranslation()

  return (
    <>
      {isFollow && <Button color="white" name={t('follow.following')} onClick={onClick} />}
      {!isFollow && <Button color="green" name={t('follow.follow')} disabled={disabled} onClick={onClick} />}
    </>
  )
}
