import Head from 'next/head'
import { NextSeo } from 'next-seo'

interface Props {
  title?: string
  description?: string
  url?: string
  locale?: string
  siteName?: string
  canonical?: string
}

export default function Meta(props: Props): JSX.Element {
  const { title, description, url, locale, siteName, canonical } = props

  return (
    <Head>
      <title>{title ? `MyUs | ${title}` : 'MyUs'}</title>
      <NextSeo title={title} description={description} canonical={canonical} openGraph={{ title, description, url, locale, siteName }} />
    </Head>
  )
}
