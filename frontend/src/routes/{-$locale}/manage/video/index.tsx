import { createFileRoute } from '@tanstack/react-router'
import ManageVideosPage from 'pages/manage/video'

export const Route = createFileRoute('/{-$locale}/manage/video/')({ component: ManageVideosPage })
