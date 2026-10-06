import { createFileRoute } from '@tanstack/react-router'
import ComicsPage from 'pages/media/comic'

export const Route = createFileRoute('/{-$locale}/media/comic/')({ component: ComicsPage })
