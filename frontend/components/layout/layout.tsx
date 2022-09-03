import Head from 'next/head'
import Header from 'components/layout/header'
import SideBar from 'components/layout/sidebar'
import SearchTag from 'components/layout/searchtag'
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
        <meta property="og:image" content="{'img/My_Idea_Know_Us.png'}"/>
        <meta property="og:description" content="MyUsとはMy Idea Know Usが名前の由来です。総合メディアサイトであり、アイディア想像サイトになります!!!"/>
        <link rel="shortcut icon" href="{'img/MyUs.png'}"/>
        <link rel="icon" type="image/png" href="{'img/MyUs.png'}"/>
        <link rel="apple-touch-icon" href="{'img/MyUs.png'}"/>
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
