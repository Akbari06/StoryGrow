export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://storygrow-433353767151.europe-west1.run.app',
  isProduction: process.env.NODE_ENV === 'production',
}