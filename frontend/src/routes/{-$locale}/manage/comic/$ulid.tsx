import { createFileRoute } from '@tanstack/react-router'
import ManageComicEditPage from 'pages/manage/comic/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/comic/$ulid')({ component: ManageComicEditPage })
