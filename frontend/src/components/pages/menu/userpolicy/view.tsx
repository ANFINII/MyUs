import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

export default function UserPolicy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.userpolicy.title')} type="table" isFooter={false}>
      <article className="article_userpolicy">
        <p>{t('menu.userpolicy.intro.p1')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article1.title')}</h2>
        <p>{t('menu.userpolicy.article1.p1')}</p>
        <p>{t('menu.userpolicy.article1.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article2.title')}</h2>
        <p>{t('menu.userpolicy.article2.p1')}</p>
        <p>{t('menu.userpolicy.article2.p2')}</p>
        <p>{t('menu.userpolicy.article2.p3')}</p>
        <p>{t('menu.userpolicy.article2.p4')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article3.title')}</h2>
        <p>{t('menu.userpolicy.article3.p1')}</p>
        <p>{t('menu.userpolicy.article3.p2')}</p>
        <p>{t('menu.userpolicy.article3.p3')}</p>
        <p>{t('menu.userpolicy.article3.p4')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article4.title')}</h2>
        <p>{t('menu.userpolicy.article4.p1')}</p>
        <p>{t('menu.userpolicy.article4.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article5.title')}</h2>
        <p>{t('menu.userpolicy.article5.p1')}</p>
        <p>{t('menu.userpolicy.article5.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article6.title')}</h2>
        <p>{t('menu.userpolicy.article6.p1')}</p>
        <p>{t('menu.userpolicy.article6.p2')}</p>
        <p>{t('menu.userpolicy.article6.p3')}</p>
        <p>{t('menu.userpolicy.article6.p4')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article7.title')}</h2>
        <p>{t('menu.userpolicy.article7.p1')}</p>
        <p>{t('menu.userpolicy.article7.p2')}</p>
        <p>{t('menu.userpolicy.article7.p3')}</p>
        <p>{t('menu.userpolicy.article7.p4')}</p>
        <p>{t('menu.userpolicy.article7.p5')}</p>
        <p>{t('menu.userpolicy.article7.p6')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article8.title')}</h2>
        <p>{t('menu.userpolicy.article8.p1')}</p>
        <p>{t('menu.userpolicy.article8.p2')}</p>
        <Divide />

        <h2>{t('menu.userpolicy.article9.title')}</h2>
        <p>{t('menu.userpolicy.article9.p1')}</p>
        <p>{t('menu.userpolicy.article9.p2')}</p>
      </article>
    </Main>
  )
}
