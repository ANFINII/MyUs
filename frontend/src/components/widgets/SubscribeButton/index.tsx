import { useTranslation } from 'react-i18next'
import Button from 'components/parts/Button'

interface Props {
  isSubscribe: boolean
  disabled: boolean
  onModal: () => void
  onSubscribe: () => void
}

export default function SubscribeButton(props: Props): React.JSX.Element {
  const { isSubscribe, disabled, onModal, onSubscribe } = props

  const { t } = useTranslation()

  return (
    <>
      {isSubscribe && <Button color="white" name={t('subscribe.subscribed')} onClick={onModal} />}
      {!isSubscribe && <Button color="green" name={t('subscribe.subscribe')} disabled={disabled} onClick={onSubscribe} />}
    </>
  )
}
