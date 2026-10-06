import { createFileRoute } from '@tanstack/react-router'
import BlogsPage from 'pages/media/blog'

export const Route = createFileRoute('/{-$locale}/media/blog/')({ component: BlogsPage })
