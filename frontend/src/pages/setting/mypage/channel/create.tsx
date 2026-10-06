import ErrorCheck from 'components/widgets/Status/Check'
import ChannelCreate from 'components/templates/setting/mypage/channel/create'

interface Props {
  status: number
}

export default function ChannelCreatePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ChannelCreate />
    </ErrorCheck>
  )
}
