import { createFileRoute } from '@tanstack/react-router'
import ChatCreatePage from 'pages/manage/chat/create'

export const Route = createFileRoute('/{-$locale}/manage/chat/create')({ component: ChatCreatePage })
