import { useRouter } from 'next/router'
import { Follow } from 'types/internal/auth'
import { getFollower } from 'api/internal/user'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import FollowList from 'components/widgets/Media/List/Follow'
import MediaFollow from 'components/widgets/Media/Index/Follow'

interface Props {
  follows: Follow[]
}

export default function Followers(props: Props) {
  const { follows } = props

  const router = useRouter()
  const { search, newDatas } = useNewDatas<Follow[]>({ datas: follows, getDatas: (search) => getFollower(undefined, search) })

  return (
    <Main title="Follower" search={{ name: search, count: newDatas.length }}>
      <LoginRequired margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="フォロワー" onClick={() => router.push('/menu/follow')} />
          <span className="ml_8">フォロワー数：{follows.length}</span>
        </div>
        <FollowList datas={newDatas} MediaMedia={MediaFollow} />
      </LoginRequired>
    </Main>
  )
}
