export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://storygrow-dd6izss4yq-ew.a.run.app',
  isProduction: process.env.NODE_ENV === 'production',
}