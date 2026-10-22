import { useRouterState } from '@tanstack/react-router'
import Main from 'components/layout/Main'
import Spinner from 'components/parts/Spinner'
import style from './Status.module.scss'

interface Props {
  title?: string
}

export default function PageLoading(props: Props): React.JSX.Element | null {
  const { title } = props

  const isInitial = useRouterState({ select: (s) => s.resolvedLocation === undefined })

  if (!isInitial) return null

  return (
    <Main metaTitle={title} isFooter={false}>
      <div className={style.loading}>
        <Spinner color="blue" size="l" />
      </div>
    </Main>
  )
}
