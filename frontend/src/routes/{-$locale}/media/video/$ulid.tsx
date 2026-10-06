import { createFileRoute } from '@tanstack/react-router'
import VideoDetailPage from 'pages/media/video/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/video/$ulid')({ component: VideoDetailPage })
