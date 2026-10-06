import { createFileRoute } from '@tanstack/react-router'
import BlogCreatePage from 'pages/manage/blog/create'

export const Route = createFileRoute('/{-$locale}/manage/blog/create')({ component: BlogCreatePage })
