import { useSession } from '@/auth/session'
import { Loading } from '@/components/Loading'
import type { JSX } from 'react'
import { Navigate } from 'react-router'

export function RequireGuest({ children }: { children: JSX.Element }) {
    const { loading, authenticated } = useSession()
    if (loading) return <Loading />
    if (authenticated) return <Navigate to="/" replace />
    return children
}
