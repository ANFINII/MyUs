import { createFileRoute } from '@tanstack/react-router'
import ChannelCreatePage from 'pages/setting/mypage/channel/create'

export const Route = createFileRoute('/{-$locale}/setting/mypage/channel/create')({ component: ChannelCreatePage })
