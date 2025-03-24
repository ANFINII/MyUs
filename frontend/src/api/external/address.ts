import { apiAddressClient } from 'lib/axios/external'
import { ApiOut, apiOut } from 'lib/error'
import { Address } from 'types/internal/address'
import { apiAddress } from 'api/uri'

// 住所検索APIリファレンス: http://zipcloud.ibsnet.co.jp/doc/api
export const getAddress = async (zipcode: string): Promise<ApiOut<Address>> => {
  return await apiOut(apiAddressClient.get(apiAddress, { params: { zipcode } }))
}
