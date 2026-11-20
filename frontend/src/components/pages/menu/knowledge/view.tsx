import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import SideTable from 'components/widgets/Table/Side'

const items = ['myus', 'video', 'audio', 'blog', 'comic', 'picture', 'chat', 'playlist', 'mypage', 'follow', 'searchTag', 'manage'] as const

export default function Knowledge(): React.JSX.Element {
  const { t } = useTranslation()

  const rows = items.map((item) => ({ label: t(`menu.knowledge.${item}.label`), content: t(`menu.knowledge.${item}.content`) }))

  return (
    <Main title="Knowledge Base" type="table">
      <SideTable rows={rows} />
    </Main>
  )
}
