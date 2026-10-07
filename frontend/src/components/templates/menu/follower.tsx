import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { Follow } from 'types/internal/user'
import { useSearchResult } from 'components/hooks/useSearchResult'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import FollowCard from 'components/widgets/Card/Follow'
import CardList from 'components/widgets/Card/List'

interface Props {
  datas: Follow[]
}

export default function Followers(props: Props): React.JSX.Element {
  const { datas } = props

  const navigate = useNavigate()
  const { t } = useTranslation()
  const search = useSearchResult(datas.length)

  return (
    <Main title="Follower" search={search}>
      <div className="mt_16">
        <Button color="blue" size="s" name={t('menu.follower.follow')} onClick={() => navigate({ to: '/menu/follow' })} />
        <span className="ml_16">{t('menu.follower.count', { count: datas.length })}</span>
      </div>
      <CardList items={datas} Content={FollowCard} />
    </Main>
  )
}
