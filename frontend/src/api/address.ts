import { apiAddressClient } from 'lib/axios'
import { AddressResult } from 'types/internal/address'
import { apiAddress } from './uri'

// 住所検索APIリファレンス: http://zipcloud.ibsnet.co.jp/doc/api
export const getAddressForm = async (zipcode: string): Promise<AddressResult[]> => {
  const data = await apiAddressClient.get(apiAddress, { params: { zipcode } }).then((res) => {
    return res.data
  })
  return data.results
}
