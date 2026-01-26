import { type UserPublic, UserService } from '@/api/generated'
import { SessionContext } from '@/auth/session'
import { type ReactNode, useEffect, useState } from 'react'

export function SessionProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<UserPublic | null>(null)
    const [loading, setLoading] = useState(true)

    const loadSession = async () => {
        setLoading(true)
        try {
            const { data, error } = await UserService.getCurrentUser()
            if (error) {
                setUser(null)
                return
            }
            setUser(data)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        void loadSession()
    }, [])

    return (
        <SessionContext.Provider
            value={{
                user,
                loading,
                authenticated: user !== null,
                refresh: loadSession,
            }}
        >
            {children}
        </SessionContext.Provider>
    )
}
