import Head from 'next/head'
import Header from 'components/layout/header'
import SideBar from 'components/layout/sidebar'
import SerchTag from 'components/layout/serchtag'
type Props = {children: React.ReactNode;}

export default function Layout({ children }: Props) {
  return (
    <>
      <Head>
        <title>MyUs</title>
      </Head>
      <Header />
      <SideBar />
      <SerchTag />
      <main>
        {children}
      </main>
    </>
  )
}
