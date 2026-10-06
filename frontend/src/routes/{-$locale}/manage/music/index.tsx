import { createFileRoute } from '@tanstack/react-router'
import ManageMusicsPage from 'pages/manage/music'

export const Route = createFileRoute('/{-$locale}/manage/music/')({ component: ManageMusicsPage })
