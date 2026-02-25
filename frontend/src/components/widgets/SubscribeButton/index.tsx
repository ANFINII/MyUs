import Button from 'components/parts/Button'

interface Props {
  isSubscribe: boolean
  disabled: boolean
  onModal: () => void
  onSubscribe: () => void
}

export default function SubscribeButton(props: Props): React.JSX.Element {
  const { isSubscribe, disabled, onModal, onSubscribe } = props

  return (
    <>
      {isSubscribe && <Button color="white" name="登録済み" onClick={onModal} />}
      {!isSubscribe && <Button color="green" name="登録する" disabled={disabled} onClick={onSubscribe} />}
    </>
  )
}
