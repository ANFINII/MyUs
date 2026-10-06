import { createFileRoute } from '@tanstack/react-router'
import VideosPage from 'pages/media/video'

export const Route = createFileRoute('/{-$locale}/media/video/')({ component: VideosPage })
