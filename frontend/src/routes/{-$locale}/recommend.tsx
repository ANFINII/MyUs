import { createFileRoute } from '@tanstack/react-router'
import RecommendPage from 'pages/recommend'

export const Route = createFileRoute('/{-$locale}/recommend')({ component: RecommendPage })
