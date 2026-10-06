import { createFileRoute } from '@tanstack/react-router'
import ManageChatEditPage from 'pages/manage/chat/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/chat/$ulid')({ component: ManageChatEditPage })
