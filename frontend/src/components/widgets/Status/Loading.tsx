import Main from 'components/layout/Main'
import Spinner from 'components/parts/Spinner'
import style from './Status.module.scss'

interface Props {
  title?: string
}

export default function PageLoading(props: Props): React.JSX.Element {
  const { title } = props

  return (
    <Main metaTitle={title} isFooter={false}>
      <div className={style.loading}>
        <Spinner color="blue" size="l" />
      </div>
    </Main>
  )
}
