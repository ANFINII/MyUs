import { HttpStatusCode } from 'axios'
import { apiAddressClient } from 'lib/axios/external'
import { Address, AddressResult } from 'types/internal/address'
import { apiAddress } from '../uri'

// 住所検索APIリファレンス: http://zipcloud.ibsnet.co.jp/doc/api
export const getAddress = async (zipcode: string): Promise<AddressResult[]> => {
  const res: Address = await apiAddressClient.get(apiAddress, { params: { zipcode } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.results
}
