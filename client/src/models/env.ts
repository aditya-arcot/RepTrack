import * as z from 'zod'

export const EnvSchema = z.object({
    ENV: z.enum(['dev', 'test', 'stage', 'prod']),
    IMAGE_TAG: z.string(),
    API_URL: z.string(),
})
