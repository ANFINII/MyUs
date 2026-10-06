import { createFileRoute } from '@tanstack/react-router'
import PictureCreatePage from 'pages/manage/picture/create'

export const Route = createFileRoute('/{-$locale}/manage/picture/create')({ component: PictureCreatePage })
