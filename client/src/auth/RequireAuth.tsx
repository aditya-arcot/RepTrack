import { useSession } from '@/auth/session'
import { Loading } from '@/components/Loading'
import { type JSX } from 'react'
import { Navigate, useLocation } from 'react-router'

export function RequireAuth({ children }: { children: JSX.Element }) {
    const { loading, authenticated } = useSession()
    const location = useLocation()
    if (loading) return <Loading />
    if (!authenticated)
        return <Navigate to="/login" replace state={{ from: location }} />
    return children
}
