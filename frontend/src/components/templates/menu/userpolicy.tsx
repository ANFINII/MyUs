import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

export default function UserPolicy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.userpolicy.title')} type="table">
      <article className="article_userpolicy">
        <p>{t('menu.userpolicy.intro.p1')}</p>
        <p>{t('menu.userpolicy.intro.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article1.title')}</h2>
        <p>{t('menu.userpolicy.article1.p1')}</p>
        <p>{t('menu.userpolicy.article1.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article2.title')}</h2>
        <p>{t('menu.userpolicy.article2.p1')}</p>
        <p>{t('menu.userpolicy.article2.p2')}</p>
        <p>{t('menu.userpolicy.article2.p3')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article3.title')}</h2>
        <p>{t('menu.userpolicy.article3.p1')}</p>
        <p>{t('menu.userpolicy.article3.p2')}</p>
        <p>{t('menu.userpolicy.article3.p3')}</p>
        <p>{t('menu.userpolicy.article3.p4')}</p>
        <p>{t('menu.userpolicy.article3.p5')}</p>
      </article>
    </Main>
  )
}
