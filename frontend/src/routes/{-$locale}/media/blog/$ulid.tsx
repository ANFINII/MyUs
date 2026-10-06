import { createFileRoute } from '@tanstack/react-router'
import BlogDetailPage from 'pages/media/blog/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/blog/$ulid')({ component: BlogDetailPage })
