import { createFileRoute } from '@tanstack/react-router'
import ManagePictureEditPage from 'pages/manage/picture/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/picture/$ulid')({ component: ManagePictureEditPage })
