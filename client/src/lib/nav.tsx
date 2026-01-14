import { cn } from '@/lib/utils'
import { NavLink } from 'react-router-dom'

interface NavItemProps {
    to: string
    children: React.ReactNode
}

export function NavItem({ to, children }: NavItemProps) {
    return (
        <NavLink
            to={to}
            className={({ isActive }) =>
                cn(
                    'text-xl font-medium transition-colors',
                    'hover:text-primary',
                    isActive ? 'text-primary' : 'text-muted-foreground'
                )
            }
        >
            {children}
        </NavLink>
    )
}
