import { useRouter } from 'next/router'
import { Follow } from 'types/internal/user'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import FollowCard from 'components/widgets/Card/Follow'
import CardList from 'components/widgets/Card/List'

interface Props {
  datas: Follow[]
}

export default function Follows(props: Props): React.JSX.Element {
  const { datas } = props

  const router = useRouter()
  const search = useSearch(datas.length)

  return (
    <Main title="Follow" search={search}>
      <div className="mt_16">
        <Button color="blue" size="s" name="フォロワー" onClick={() => router.push('/menu/follower')} />
        <span className="ml_16">フォロー数：{datas.length}</span>
      </div>
      <CardList items={datas} Content={FollowCard} />
    </Main>
  )
}
