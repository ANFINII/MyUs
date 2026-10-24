import { Currency } from 'utils/constants/enum'
import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    price: 550,
    currency: Currency.Jpy,
    features: [{ key: 'individualAds', count: 1 }, { key: 'hideGlobalAds' }, { key: 'promotion' }],
  },
  {
    name: 'Standard',
    price: 880,
    currency: Currency.Jpy,
    features: [{ key: 'individualAds', count: 2 }, { key: 'hideGlobalAds' }, { key: 'promotion' }],
  },
  {
    name: 'Premium',
    price: 1200,
    currency: Currency.Jpy,
    features: [{ key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }, { key: 'musicDownload' }, { key: 'promotion' }],
  },
  {
    name: 'Free',
    price: 0,
    currency: Currency.Jpy,
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
