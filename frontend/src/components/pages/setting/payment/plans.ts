import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    features: [{ key: 'individualAds', count: 1 }, { key: 'hideGlobalAds' }, { key: 'series' }, { key: 'playlist' }],
  },
  {
    name: 'Standard',
    features: [{ key: 'individualAds', count: 2 }, { key: 'hideGlobalAds' }, { key: 'series' }, { key: 'playlist' }],
  },
  {
    name: 'Premium',
    features: [{ key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }, { key: 'series' }, { key: 'playlist' }, { key: 'musicDownload' }],
  },
  {
    name: 'Free',
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
