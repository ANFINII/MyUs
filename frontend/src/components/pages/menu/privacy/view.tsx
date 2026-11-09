import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

const sections = ['collect', 'purpose', 'thirdParty', 'external', 'security', 'request', 'contact', 'revision'] as const

export default function Privacy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.privacy.title')} type="table">
      <article className="article_userpolicy">
        {sections.map((section, index) => (
          <section key={section}>
            {index > 0 && <Divide />}
            <h2>{t(`menu.privacy.${section}.title`)}</h2>
            <p>{t(`menu.privacy.${section}.content`)}</p>
          </section>
        ))}
      </article>
    </Main>
  )
}
