import { createFileRoute } from '@tanstack/react-router'
import ChannelsPage from 'pages/menu/channel'

export const Route = createFileRoute('/{-$locale}/menu/channel')({ component: ChannelsPage })
