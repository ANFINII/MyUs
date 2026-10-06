import { createFileRoute } from '@tanstack/react-router'
import ManageBlogsPage from 'pages/manage/blog'

export const Route = createFileRoute('/{-$locale}/manage/blog/')({ component: ManageBlogsPage })
