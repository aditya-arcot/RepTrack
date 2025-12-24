import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
    input: 'openapi_spec.json',
    output: 'src/api/generated',
    plugins: [
        {
            name: '@hey-api/client-axios',
            runtimeConfigPath: '@/api/axios.ts',
        },
        {
            name: '@hey-api/sdk',
            asClass: true,
            operationId: true,
            classNameBuilder: '{{name}}Service',
        },
        {
            name: '@hey-api/schemas',
            type: 'json',
        },
    ],
})
