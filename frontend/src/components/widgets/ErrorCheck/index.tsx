import Custom404 from 'components/widgets/Error/404'
import Custom500 from 'components/widgets/Error/500'

interface Props {
  status: number
  children: React.ReactNode
}

export default function ErrorCheck(props: Props): JSX.Element {
  const { status, children } = props

  if (status >= 500) return <Custom500 />
  if (status >= 404) return <Custom404 />
  return <>{children}</>
}
