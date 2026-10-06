import { createFileRoute } from '@tanstack/react-router'
import ManageBlogEditPage from 'pages/manage/blog/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/blog/$ulid')({ component: ManageBlogEditPage })
