import { createFileRoute } from '@tanstack/react-router'
import SettingProfilePage from 'pages/setting/profile'

export const Route = createFileRoute('/{-$locale}/setting/profile/')({ component: SettingProfilePage })
