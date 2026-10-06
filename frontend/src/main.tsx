import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from '@tanstack/react-router'
import { router } from 'lib/router'
import 'video.js/dist/video-js.css'
import 'styles/global/reset.scss'
import 'styles/global/style.scss'
import 'styles/global/index.scss'
import 'styles/global/main_other.scss'
import 'styles/internal/userpolicy.scss'
import 'styles/internal/registration.scss'
import 'styles/internal/videojs-myus.scss'

const root = document.getElementById('root')

if (root) {
  createRoot(root).render(
    <StrictMode>
      <RouterProvider router={router} />
    </StrictMode>,
  )
}
