import { useRouter } from 'next/router'
import { Follow } from 'types/internal/user'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import MediaFollow from 'components/widgets/Media/Index/Follow'
import FollowList from 'components/widgets/Media/List/Follow'

interface Props {
  datas: Follow[]
}

export default function Followers(props: Props): React.JSX.Element {
  const { datas } = props

  const router = useRouter()
  const search = useSearch(datas)

  return (
    <Main title="Follower" search={search}>
      <LoginError margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="フォロー" onClick={() => router.push('/menu/follow')} />
          <span className="ml_16">フォロワー数：{datas.length}</span>
        </div>
        <FollowList medias={datas} MediaComponent={MediaFollow} />
      </LoginError>
    </Main>
  )
}
