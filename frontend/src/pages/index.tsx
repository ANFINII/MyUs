import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { MediaHome } from 'types/internal/media'
import { getHome } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = searchParams(query)
  const ret = await getHome(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const mediaHome = ret.value
  return { props: { mediaHome, ...translations } }
}

interface Props {
  status: number
  mediaHome: MediaHome
}

export default function HomesPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Homes {...props} />
    </ErrorCheck>
  )
}
