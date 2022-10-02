import Head from 'next/head'
import Header from 'components/layouts/header/header'
import SideBar from 'components/layouts/sidebar'
import SearchTag from 'components/layouts/searchtag'

type Props = {children: React.ReactNode;}

export default function Layout({ children }: Props) {
  return (
    <div className="layout">
      <Head>
        <meta charSet="UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="ie=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
        <meta name="description" content="MyUsとはMy Idea Know Usが名前の由来です。総合メディアサイトであり、アイディア想像サイトになります!!!"/>
        <meta name="keywords" content="MyUs, My Idea Know Us, SNS"/>
        <meta name="author" content="ANFINII"/>
        <meta name="generator" content="Django"/>
        <meta name="application-name" content="MyUs"/>
        <meta name="mobile-web-app-capable" content="yes"/>
        <meta name="apple-mobile-web-app-title" content="MyUs"/>
        <meta name="apple-mobile-web-app-capable" content="yes"/>
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
        <meta property="og:title" content="My Idea Know Us"/>
        <meta property="og:site_name" content="MyUs"/>
        <meta property="og:url" content="https://www.myus.com"/>
        <meta property="og:type" content="website"/>
        <meta property="og:image" content="/img/My_Idea_Know_Us.png"/>
        <meta property="og:description" content="MyUsとはMy Idea Know Usが名前の由来です。総合メディアサイトであり、アイディア想像サイトになります!!!"/>
        <meta name="theme-color" content="#ffffff"/>
        <meta name="msapplication-TileColor" content="#ffffff"/>
        <meta name="msapplication-config" content="/favicon/browserconfig.xml"/>
        <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png"/>
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png"/>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png"/>
        <link rel="manifest" href="/favicon/site.webmanifest"/>
        <link rel="mask-icon" href="/favicon/safari-pinned-tab.svg" color="#000000"/>
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css"/>
        <base href="/"></base>
        <title>MyUs</title>
      </Head>
      <Header/>
      <SideBar/>
      <SearchTag/>
      <main className="main">
        { children }
      </main>
    </div>
  )
}
