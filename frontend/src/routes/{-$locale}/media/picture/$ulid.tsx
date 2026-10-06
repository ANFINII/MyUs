import { createFileRoute } from '@tanstack/react-router'
import PictureDetailPage from 'pages/media/picture/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/picture/$ulid')({ component: PictureDetailPage })
