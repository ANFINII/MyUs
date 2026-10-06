import { createFileRoute } from '@tanstack/react-router'
import KnowledgePage from 'pages/menu/knowledge'

export const Route = createFileRoute('/{-$locale}/menu/knowledge')({ component: KnowledgePage })
