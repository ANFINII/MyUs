import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { Category } from 'types/internal/category'
import { apiMediaCategory } from 'api/uri'

export const getCategories = async (): Promise<ApiOut<Category[]>> => {
  return await apiOut(apiClient('json').get(apiMediaCategory))
}
