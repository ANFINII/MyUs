import { createFileRoute } from '@tanstack/react-router'
import ManageMusicEditPage from 'pages/manage/music/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/music/$ulid')({ component: ManageMusicEditPage })
