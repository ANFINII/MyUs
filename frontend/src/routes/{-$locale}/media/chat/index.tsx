import { createFileRoute } from '@tanstack/react-router'
import ChatsPage from 'pages/media/chat'

export const Route = createFileRoute('/{-$locale}/media/chat/')({ component: ChatsPage })
