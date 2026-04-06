import Head from 'next/head'

interface Props {
  title?: string
  description?: string
  url?: string
  locale?: string
  siteName?: string
  canonical?: string
}

export default function Meta(props: Props): React.JSX.Element {
  const { title, description, url, locale, siteName, canonical } = props

  const pageTitle = title ? `MyUs | ${title}` : 'MyUs'

  return (
    <Head>
      <title>{pageTitle}</title>
      <meta property="og:title" content={pageTitle} />
      <meta property="og:type" content="website" />
      {description && <meta name="description" content={description} />}
      {canonical && <link rel="canonical" href={canonical} />}
      {description && <meta property="og:description" content={description} />}
      {url && <meta property="og:url" content={url} />}
      {locale && <meta property="og:locale" content={locale} />}
      {siteName && <meta property="og:site_name" content={siteName} />}
    </Head>
  )
}
