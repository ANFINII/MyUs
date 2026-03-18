import Button from 'components/parts/Button'

interface Props {
  isFollow: boolean
  disabled: boolean
  onClick: () => void
}

export default function FollowButton(props: Props): React.JSX.Element {
  const { isFollow, disabled, onClick } = props

  return (
    <>
      {isFollow && <Button color="white" name="フォロー済み" onClick={onClick} />}
      {!isFollow && <Button color="green" name="フォローする" disabled={disabled} onClick={onClick} />}
    </>
  )
}
