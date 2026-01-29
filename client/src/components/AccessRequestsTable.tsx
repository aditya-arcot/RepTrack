import { AccessRequestStatusSchema } from '@/api/generated/schemas.gen'
import type {
    AccessRequestPublic,
    AccessRequestStatus,
} from '@/api/generated/types.gen'
import { zAccessRequestPublic } from '@/api/generated/zod.gen'
import { DataTable } from '@/components/data-table/DataTable'
import { DataTableColumnHeader } from '@/components/data-table/DataTableColumnHeader'
import { DataTableInlineRowActions } from '@/components/data-table/DataTableInlineRowActions'
import { createSelectColumn } from '@/components/data-table/DataTableSelectColumn'
import { Badge } from '@/components/ui/badge'
import {
    blueBadgeClassName,
    greenBadgeClassName,
    redBadgeClassName,
} from '@/lib/styles'
import type {
    DataTableRowActionsConfig,
    DataTableToolbarConfig,
    FilterOption,
} from '@/models/data-table'
import type { ColumnDef } from '@tanstack/react-table'
import { Check, X } from 'lucide-react'

function StatusBadge({ status }: { status: AccessRequestStatus }) {
    switch (status) {
        case 'pending':
            return <Badge className={blueBadgeClassName}>Pending</Badge>
        case 'approved':
            return <Badge className={greenBadgeClassName}>Approved</Badge>
        case 'rejected':
            return <Badge className={redBadgeClassName}>Rejected</Badge>
    }
}

function getStatusFilterOptions(): FilterOption[] {
    return AccessRequestStatusSchema.enum.map((status) => ({
        label: status.charAt(0).toUpperCase() + status.slice(1),
        value: status,
    }))
}

const rowActionsConfig: DataTableRowActionsConfig<AccessRequestPublic> = {
    schema: zAccessRequestPublic,
    menuItems: (row) => {
        if (row.status !== 'pending') {
            return []
        }
        return [
            {
                type: 'action',
                label: 'Approve',
                className: 'text-green-700',
                icon: Check,
                onSelect: (data) => {
                    // TODO implement approve action
                    // eslint-disable-next-line no-console
                    console.log('Approve request:', data)
                },
            },
            {
                type: 'action',
                className: 'text-red-700',
                label: 'Reject',
                icon: X,
                onSelect: (data) => {
                    // TODO implement reject action
                    // eslint-disable-next-line no-console
                    console.log('Reject request:', data)
                },
            },
        ]
    },
}

const columns: ColumnDef<AccessRequestPublic>[] = [
    createSelectColumn<AccessRequestPublic>(),
    {
        id: 'name',
        accessorFn: (row) => `${row.first_name} ${row.last_name}`,
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Name" />
        ),
        enableHiding: false,
    },
    {
        accessorKey: 'email',
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Email" />
        ),
        enableHiding: false,
    },
    {
        accessorKey: 'status',
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Status" />
        ),
        cell: ({ row }) => {
            return (
                <div className="-ml-2">
                    <StatusBadge status={row.original.status} />
                </div>
            )
        },
        filterFn: (row, id, value: string[]) => {
            return value.includes(row.getValue(id))
        },
        enableHiding: false,
    },
    // TODO reviewed by
    {
        accessorKey: 'reviewed_at',
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Reviewed At" />
        ),
        cell: ({ row }) =>
            row.original.reviewed_at
                ? new Date(row.original.reviewed_at).toLocaleString()
                : '—',
        enableHiding: false,
    },
    {
        accessorKey: 'updated_at',
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Updated At" />
        ),
        cell: ({ row }) => new Date(row.original.updated_at).toLocaleString(),
        enableHiding: false,
    },
    {
        id: 'actions',
        header: ({ column }) => (
            <DataTableColumnHeader
                column={column}
                title="Actions"
                className="justify-center"
            />
        ),
        cell: ({ row }) => {
            const menuItems = rowActionsConfig.menuItems(row.original)
            return menuItems.length > 0 ? (
                <DataTableInlineRowActions
                    row={row}
                    config={rowActionsConfig}
                />
            ) : (
                <div className="text-center">—</div>
            )
        },
        enableHiding: false,
    },
]

const toolbarConfig: DataTableToolbarConfig = {
    search: {
        columnId: 'name',
        placeholder: 'Filter by name...',
    },
    filters: [
        {
            columnId: 'status',
            title: 'Status',
            options: getStatusFilterOptions(),
        },
    ],
    showViewOptions: false,
}

interface AccessRequestsTableProps {
    requests: AccessRequestPublic[]
    isLoading: boolean
}

export function AccessRequestsTable({
    requests,
    isLoading,
}: AccessRequestsTableProps) {
    return (
        <DataTable
            data={requests}
            columns={columns}
            isLoading={isLoading}
            toolbarConfig={toolbarConfig}
        />
    )
}
