import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

export default function Privacy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.privacy.title')} type="table" isFooter={false}>
      <article className="article_userpolicy">
        <h2>{t('menu.privacy.collect.title')}</h2>
        <p>{t('menu.privacy.collect.p1')}</p>
        <p>{t('menu.privacy.collect.p2')}</p>
        <p>{t('menu.privacy.collect.p3')}</p>
        <p>{t('menu.privacy.collect.p4')}</p>
        <Divide />

        <h2>{t('menu.privacy.purpose.title')}</h2>
        <p>{t('menu.privacy.purpose.p1')}</p>
        <p>{t('menu.privacy.purpose.p2')}</p>
        <p>{t('menu.privacy.purpose.p3')}</p>
        <p>{t('menu.privacy.purpose.p4')}</p>
        <Divide />

        <h2>{t('menu.privacy.thirdParty.title')}</h2>
        <p>{t('menu.privacy.thirdParty.p1')}</p>
        <p>{t('menu.privacy.thirdParty.p2')}</p>
        <Divide />

        <h2>{t('menu.privacy.external.title')}</h2>
        <p>{t('menu.privacy.external.p1')}</p>
        <p>{t('menu.privacy.external.p2')}</p>
        <p>{t('menu.privacy.external.p3')}</p>
        <p>{t('menu.privacy.external.p4')}</p>
        <p>{t('menu.privacy.external.p5')}</p>
        <Divide />

        <h2>{t('menu.privacy.security.title')}</h2>
        <p>{t('menu.privacy.security.p1')}</p>
        <p>{t('menu.privacy.security.p2')}</p>
        <Divide />

        <h2>{t('menu.privacy.request.title')}</h2>
        <p>{t('menu.privacy.request.p1')}</p>
        <p>{t('menu.privacy.request.p2')}</p>
        <Divide />

        <h2>{t('menu.privacy.contact.title')}</h2>
        <p>{t('menu.privacy.contact.p1')}</p>
        <Divide />

        <h2>{t('menu.privacy.revision.title')}</h2>
        <p>{t('menu.privacy.revision.p1')}</p>
      </article>
    </Main>
  )
}
