import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'

const articles = [
  { key: 'article1', title: 'menu.userpolicy.article1.title', paragraphs: ['menu.userpolicy.article1.p1', 'menu.userpolicy.article1.p2'] },
  { key: 'article2', title: 'menu.userpolicy.article2.title', paragraphs: ['menu.userpolicy.article2.p1', 'menu.userpolicy.article2.p2', 'menu.userpolicy.article2.p3', 'menu.userpolicy.article2.p4'] },
  { key: 'article3', title: 'menu.userpolicy.article3.title', paragraphs: ['menu.userpolicy.article3.p1', 'menu.userpolicy.article3.p2', 'menu.userpolicy.article3.p3', 'menu.userpolicy.article3.p4', 'menu.userpolicy.article3.p5', 'menu.userpolicy.article3.p6', 'menu.userpolicy.article3.p7', 'menu.userpolicy.article3.p8'] },
  { key: 'article4', title: 'menu.userpolicy.article4.title', paragraphs: ['menu.userpolicy.article4.p1', 'menu.userpolicy.article4.p2', 'menu.userpolicy.article4.p3'] },
  { key: 'article5', title: 'menu.userpolicy.article5.title', paragraphs: ['menu.userpolicy.article5.p1', 'menu.userpolicy.article5.p2'] },
  { key: 'article6', title: 'menu.userpolicy.article6.title', paragraphs: ['menu.userpolicy.article6.p1', 'menu.userpolicy.article6.p2', 'menu.userpolicy.article6.p3'] },
  { key: 'article7', title: 'menu.userpolicy.article7.title', paragraphs: ['menu.userpolicy.article7.p1', 'menu.userpolicy.article7.p2', 'menu.userpolicy.article7.p3'] },
  { key: 'article8', title: 'menu.userpolicy.article8.title', paragraphs: ['menu.userpolicy.article8.p1', 'menu.userpolicy.article8.p2', 'menu.userpolicy.article8.p3', 'menu.userpolicy.article8.p4'] },
  { key: 'article9', title: 'menu.userpolicy.article9.title', paragraphs: ['menu.userpolicy.article9.p1', 'menu.userpolicy.article9.p2', 'menu.userpolicy.article9.p3', 'menu.userpolicy.article9.p4', 'menu.userpolicy.article9.p5'] },
  { key: 'article10', title: 'menu.userpolicy.article10.title', paragraphs: ['menu.userpolicy.article10.p1', 'menu.userpolicy.article10.p2'] },
  { key: 'article11', title: 'menu.userpolicy.article11.title', paragraphs: ['menu.userpolicy.article11.p1', 'menu.userpolicy.article11.p2'] },
  { key: 'article12', title: 'menu.userpolicy.article12.title', paragraphs: ['menu.userpolicy.article12.p1'] },
  { key: 'article13', title: 'menu.userpolicy.article13.title', paragraphs: ['menu.userpolicy.article13.p1'] },
] as const

export default function UserPolicy(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title={t('menu.userpolicy.title')} type="table">
      <article className="article_userpolicy">
        <p>{t('menu.userpolicy.intro.p1')}</p>
        <p>{t('menu.userpolicy.intro.p2')}</p>
        {articles.map((article) => (
          <section key={article.key}>
            <Divide />
            <h2>{t(article.title)}</h2>
            {article.paragraphs.map((paragraph) => (
              <p key={paragraph}>{t(paragraph)}</p>
            ))}
          </section>
        ))}
      </article>
    </Main>
  )
}
