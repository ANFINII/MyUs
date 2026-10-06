import { createFileRoute } from '@tanstack/react-router'
import ComicCreatePage from 'pages/manage/comic/create'

export const Route = createFileRoute('/{-$locale}/manage/comic/create')({ component: ComicCreatePage })
