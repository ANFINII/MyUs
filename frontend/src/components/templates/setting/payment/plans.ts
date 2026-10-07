import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    price: 550,
    features: [{ key: 'individualAds', count: 1 }, { key: 'hideGlobalAds' }],
  },
  {
    name: 'Standard',
    price: 880,
    features: [{ key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }],
  },
  {
    name: 'Premium',
    price: 1200,
    features: [{ key: 'individualAds', count: 4 }, { key: 'hideGlobalAds' }, { key: 'musicDownload' }],
  },
  {
    name: 'Free',
    price: 0,
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
