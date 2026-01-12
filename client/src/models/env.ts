import * as z from 'zod'

export const EnvSchema = z.object({
    ENV: z.enum(['dev', 'test', 'stage', 'prod']),
    API_URL: z.string(),
})
