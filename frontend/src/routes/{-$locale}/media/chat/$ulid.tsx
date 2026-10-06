import { createFileRoute } from '@tanstack/react-router'
import ChatDetailPage from 'pages/media/chat/[ulid]'

export const Route = createFileRoute('/{-$locale}/media/chat/$ulid')({ component: ChatDetailPage })
