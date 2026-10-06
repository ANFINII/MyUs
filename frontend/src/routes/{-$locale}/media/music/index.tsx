import { createFileRoute } from '@tanstack/react-router'
import MusicsPage from 'pages/media/music'

export const Route = createFileRoute('/{-$locale}/media/music/')({ component: MusicsPage })
