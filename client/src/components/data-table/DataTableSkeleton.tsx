import { Skeleton } from '@/components/ui/skeleton'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'

interface DataTableSkeletonProps {
    columnCount: number
}

export function DataTableSkeleton({ columnCount }: DataTableSkeletonProps) {
    return (
        <div className="overflow-hidden rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        {Array.from({ length: columnCount }).map((_, i) => (
                            <TableHead key={i}>
                                <Skeleton className="h-6 w-20" />
                            </TableHead>
                        ))}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {Array.from({ length: 5 }).map((_, rowIndex) => (
                        <TableRow key={rowIndex}>
                            {Array.from({ length: columnCount }).map(
                                (_, cellIndex) => (
                                    <TableCell key={cellIndex}>
                                        <Skeleton className="h-6 w-full" />
                                    </TableCell>
                                )
                            )}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}
