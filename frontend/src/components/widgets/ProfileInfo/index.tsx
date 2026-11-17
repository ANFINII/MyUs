import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  avatar: string
  ulid: string
  name: string
  countLabel: string
  count: number
}

export default function ProfileInfo(props: Props): React.JSX.Element {
  const { avatar, ulid, name, countLabel, count } = props

  return (
    <HStack gap="4">
      <AvatarLink size="l" src={avatar} ulid={ulid} title={name} />
      <VStack gap="2">
        <p className="fs_14">{name}</p>
        <p className="fs_14 text_sub">
          {countLabel}
          <span className="ml_8">{count}</span>
        </p>
      </VStack>
    </HStack>
  )
}
