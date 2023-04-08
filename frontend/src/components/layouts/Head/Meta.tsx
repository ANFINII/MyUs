import Head from 'next/head'

interface Props {title?: string}

export default function Meta(props: Props) {
  const {title} = props
  return (
    <Head>
      <title>{title ? title : 'MyUs'}</title>
    </Head>
  )
}
