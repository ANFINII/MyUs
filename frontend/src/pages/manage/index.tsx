import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Manage from 'components/templates/manage'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManagePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user: query }

  return (
    <QueryCheck queries={queries} title="投稿管理">
      <Manage />
    </QueryCheck>
  )
}
