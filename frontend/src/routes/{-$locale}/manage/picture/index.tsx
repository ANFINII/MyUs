import { createFileRoute } from '@tanstack/react-router'
import ManagePicturesPage from 'pages/manage/picture'

export const Route = createFileRoute('/{-$locale}/manage/picture/')({ component: ManagePicturesPage })
