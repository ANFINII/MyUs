import { createFileRoute } from '@tanstack/react-router'
import MusicCreatePage from 'pages/manage/music/create'

export const Route = createFileRoute('/{-$locale}/manage/music/create')({ component: MusicCreatePage })
