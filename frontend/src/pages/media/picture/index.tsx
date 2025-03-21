import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Picture } from 'types/internal/media'
import { getPictures } from 'api/internal/media/list'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Pictures from 'components/templates/media/picture/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const ret = await getPictures(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Picture[]
}

export default function PicturesPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Pictures {...props} />
    </ErrorCheck>
  )
}
