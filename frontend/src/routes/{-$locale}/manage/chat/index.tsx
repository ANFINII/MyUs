import { createFileRoute } from '@tanstack/react-router'
import ManageChatsPage from 'pages/manage/chat'

export const Route = createFileRoute('/{-$locale}/manage/chat/')({ component: ManageChatsPage })
