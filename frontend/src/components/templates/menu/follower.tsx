import { useTranslation } from 'react-i18next'
import { Follow } from 'types/internal/user'
import { useRouter } from 'components/hooks/useRouter'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import FollowCard from 'components/widgets/Card/Follow'
import CardList from 'components/widgets/Card/List'

interface Props {
  datas: Follow[]
}

export default function Followers(props: Props): React.JSX.Element {
  const { datas } = props

  const router = useRouter()
  const { t } = useTranslation()
  const search = useSearch(datas.length)

  return (
    <Main title="Follower" search={search}>
      <div className="mt_16">
        <Button color="blue" size="s" name={t('menu.follower.follow')} onClick={() => router.push('/menu/follow')} />
        <span className="ml_16">{t('menu.follower.count', { count: datas.length })}</span>
      </div>
      <CardList items={datas} Content={FollowCard} />
    </Main>
  )
}
