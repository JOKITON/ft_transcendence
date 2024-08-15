import Api from './utils/Api/Api'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: Api
  }
}
