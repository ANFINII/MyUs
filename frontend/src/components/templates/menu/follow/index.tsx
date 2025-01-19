import { useRouter } from 'next/router'
import { Follow } from 'types/internal/auth'
import { getFollow } from 'api/internal/user'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import MediaFollow from 'components/widgets/Media/Index/Follow'
import FollowList from 'components/widgets/Media/List/Follow'

interface Props {
  follows: Follow[]
}

export default function Follows(props: Props): JSX.Element {
  const { follows } = props

  const router = useRouter()
  const { search, newDatas } = useNewDatas<Follow[]>({ datas: follows, getDatas: (search) => getFollow(undefined, search) })

  return (
    <Main title="Follow" search={{ name: search, count: newDatas.length }}>
      <LoginError margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="フォロワー" onClick={() => router.push('/menu/follower')} />
          <span className="ml_16">フォロー数：{follows.length}</span>
        </div>
        <FollowList medias={newDatas} MediaComponent={MediaFollow} />
      </LoginError>
    </Main>
  )
}
