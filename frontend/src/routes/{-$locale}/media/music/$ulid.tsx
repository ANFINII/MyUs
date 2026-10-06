import { createFileRoute } from '@tanstack/react-router'
import MusicDetailPage from 'pages/media/music/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/music/$ulid')({ component: MusicDetailPage })
