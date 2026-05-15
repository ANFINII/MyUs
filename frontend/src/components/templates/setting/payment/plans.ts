import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    price: 550,
    features: ['個別広告表示 1つ', '全体広告 非表示'],
  },
  {
    name: 'Standard',
    price: 880,
    features: ['個別広告表示 3つ', '全体広告 非表示'],
  },
  {
    name: 'Premium',
    price: 1200,
    features: ['個別広告表示 4つ', '全体広告 非表示', '楽曲ダウンロード'],
  },
  {
    name: 'Free',
    price: 0,
    features: ['基本機能', '広告あり'],
  },
]
