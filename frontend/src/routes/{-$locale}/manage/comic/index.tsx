import { createFileRoute } from '@tanstack/react-router'
import ManageComicsPage from 'pages/manage/comic'

export const Route = createFileRoute('/{-$locale}/manage/comic/')({ component: ManageComicsPage })
