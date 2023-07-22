import 'styles/reset.css'
import 'styles/global.css'
import 'styles/layout/layout.css'
import 'styles/layout/header.css'
import 'styles/layout/footer.css'
import 'styles/layout/sidebar.css'
import 'styles/layout/searchtag.css'
import 'styles/layout/main.css'
import 'styles/layout/mediaquery.css'
import 'styles/registration.css'
import 'styles/account.css'
import 'styles/userpolicy.css'
import 'styles/quill.css'
import 'styles/audio.css'
import 'styles/videojs-myus.css'
// import 'styles/chat.css'
import type { AppProps } from 'next/app'

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
