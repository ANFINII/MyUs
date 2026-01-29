import Custom404 from './Custom404'
import Custom500 from './Custom500'
import Unauthorized from './Unauthorized'
import Unexpected from './Unexpected'

interface Props {
  status: number
  children: React.ReactNode
}

export default function ErrorCheck(props: Props): React.JSX.Element {
  const { status, children } = props

  if (status >= 500) return <Custom500 />
  if (status === 404) return <Custom404 />
  if (status === 401) return <Unauthorized />
  if (status >= 400) return <Unexpected />
  return <>{children}</>
}
