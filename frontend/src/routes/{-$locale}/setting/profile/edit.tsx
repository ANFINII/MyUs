import { createFileRoute } from '@tanstack/react-router'
import SettingProfilePage from 'pages/setting/profile/edit'

export const Route = createFileRoute('/{-$locale}/setting/profile/edit')({ component: SettingProfilePage })
