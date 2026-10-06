import { createFileRoute } from '@tanstack/react-router'
import ComicDetailPage from 'pages/media/comic/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/comic/$ulid')({ component: ComicDetailPage })
