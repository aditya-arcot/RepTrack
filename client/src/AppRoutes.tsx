import { RequireAuth } from '@/auth/RequireAuth'
import { RequireGuest } from '@/auth/RequireGuest'
import { Doc } from '@/components/Doc'
import { DocsIndex } from '@/components/DocsIndex'
import { AppLayout } from '@/layout/AppLayout'
import { Dashboard } from '@/pages/Dashboard'
import { Docs } from '@/pages/Docs'
import { Login } from '@/pages/Login'
import { Route, Routes } from 'react-router'

export function AppRoutes() {
    return (
        <Routes>
            <Route
                path="/"
                element={
                    <RequireAuth>
                        <AppLayout />
                    </RequireAuth>
                }
            >
                <Route index element={<Dashboard />} />
                <Route path="docs" element={<Docs />}>
                    <Route index element={<DocsIndex />} />
                    <Route path=":slug" element={<Doc />} />
                </Route>
            </Route>
            <Route
                path="/login"
                element={
                    <RequireGuest>
                        <Login />
                    </RequireGuest>
                }
            />
        </Routes>
    )
}
