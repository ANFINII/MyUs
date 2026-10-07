import { useTranslation } from 'react-i18next'
import style from './Common.module.scss'

interface Props {
  publish: boolean
  children: React.ReactNode
}

export default function MediaDetail(props: Props): React.JSX.Element {
  const { publish, children } = props

  const { t } = useTranslation()

  return <article>{publish ? children : <h2 className={style.unpublished}>{t('mediaDetail.unpublished')}</h2>}</article>
}
