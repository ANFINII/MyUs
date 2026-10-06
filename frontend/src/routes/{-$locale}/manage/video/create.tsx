import { createFileRoute } from '@tanstack/react-router'
import VideoCreatePage from 'pages/manage/video/create'

export const Route = createFileRoute('/{-$locale}/manage/video/create')({ component: VideoCreatePage })
