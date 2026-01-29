import { type AccessRequestPublic, AdminService } from '@/api/generated'
import { AccessRequestsTable } from '@/components/AccessRequestsTable'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { isHttpError } from '@/lib/http'
import { logger } from '@/lib/logger'
import { notify } from '@/lib/notify'
import { useEffect, useState } from 'react'

export function Admin() {
    const [requests, setRequests] = useState<AccessRequestPublic[]>([])
    const [loadingRequests, setLoadingRequests] = useState(true)

    const loadAccessRequests = async () => {
        setLoadingRequests(true)
        try {
            const { data, error } = await AdminService.getAccessRequests()
            if (error) {
                if (isHttpError(error)) {
                    notify.error(error.detail)
                } else {
                    notify.error('Failed to fetch access requests')
                }
                setRequests([])
                return
            }
            logger.info('Fetched access requests', data)
            setRequests(data)
        } finally {
            setLoadingRequests(false)
        }
    }

    useEffect(() => {
        void loadAccessRequests()
        // TODO load users
    }, [])

    return (
        <div className="space-y-4">
            <Card className="gap-2">
                <CardHeader>
                    <CardTitle>
                        <h1 className="text-xl font-bold">Access Requests</h1>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <AccessRequestsTable
                        requests={requests}
                        isLoading={loadingRequests}
                    />
                </CardContent>
            </Card>
            <Card className="gap-2">
                <CardHeader>
                    <CardTitle>
                        <h1 className="text-xl font-bold">Users</h1>
                    </CardTitle>
                </CardHeader>
                <CardContent>{/* TODO users table */}</CardContent>
            </Card>
        </div>
    )
}
