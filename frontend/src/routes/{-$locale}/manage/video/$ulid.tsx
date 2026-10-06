import { createFileRoute } from '@tanstack/react-router'
import ManageVideoEditPage from 'pages/manage/video/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/video/$ulid')({ component: ManageVideoEditPage })
