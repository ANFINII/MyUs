import { createFileRoute } from '@tanstack/react-router'
import PicturesPage from 'pages/media/picture'

export const Route = createFileRoute('/{-$locale}/media/picture/')({ component: PicturesPage })
