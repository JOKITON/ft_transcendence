import type Api from '@/utils/Api/Api'
import Socket from '@/utils/socket/imp/socket'
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: Api
  }
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $socket: Socket
  }
}
