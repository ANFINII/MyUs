// import 'bootstrap/dist/css/bootstrap.min.css'
import 'styles/bootstrap.css'
import 'styles/globals.css'
import 'styles/layout.css'
import 'styles/main.css'
import 'styles/registration.css'
import 'styles/account.css'
import 'styles/userpolicy.css'
import 'styles/quill.css'
import 'styles/audio.css'
import 'styles/videojs-myus.css'
// import 'styles/chat.css'
import type {AppProps} from 'next/app'
import Layout from 'components/layouts'

export default function MyApp({Component, pageProps}: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}
