import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

const sections = [
  { key: 'collect', title: 'menu.privacy.collect.title', paragraphs: ['menu.privacy.collect.p1', 'menu.privacy.collect.p2', 'menu.privacy.collect.p3', 'menu.privacy.collect.p4'] },
  { key: 'purpose', title: 'menu.privacy.purpose.title', paragraphs: ['menu.privacy.purpose.p1', 'menu.privacy.purpose.p2', 'menu.privacy.purpose.p3', 'menu.privacy.purpose.p4'] },
  { key: 'thirdParty', title: 'menu.privacy.thirdParty.title', paragraphs: ['menu.privacy.thirdParty.p1', 'menu.privacy.thirdParty.p2'] },
  { key: 'external', title: 'menu.privacy.external.title', paragraphs: ['menu.privacy.external.p1', 'menu.privacy.external.p2', 'menu.privacy.external.p3', 'menu.privacy.external.p4', 'menu.privacy.external.p5'] },
  { key: 'security', title: 'menu.privacy.security.title', paragraphs: ['menu.privacy.security.p1', 'menu.privacy.security.p2'] },
  { key: 'request', title: 'menu.privacy.request.title', paragraphs: ['menu.privacy.request.p1', 'menu.privacy.request.p2'] },
  { key: 'contact', title: 'menu.privacy.contact.title', paragraphs: ['menu.privacy.contact.p1'] },
  { key: 'revision', title: 'menu.privacy.revision.title', paragraphs: ['menu.privacy.revision.p1'] },
] as const

export default function Privacy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.privacy.title')} type="table">
      <article className="article_userpolicy">
        {sections.map((section, index) => (
          <section key={section.key}>
            {index > 0 && <Divide />}
            <h2>{t(section.title)}</h2>
            {section.paragraphs.map((paragraph) => (
              <p key={paragraph}>{t(paragraph)}</p>
            ))}
          </section>
        ))}
      </article>
    </Main>
  )
}
