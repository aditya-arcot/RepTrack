import mermaid from 'mermaid'
import { useEffect, useRef } from 'react'

mermaid.initialize({
    startOnLoad: false,
    theme: 'forest',
})

export function Mermaid({ code }: { code: string }) {
    const ref = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (!ref.current) return
        const id = `mermaid-${Math.random().toString(36).slice(2)}`
        void mermaid.render(id, code).then(({ svg }) => {
            if (ref.current) {
                ref.current.innerHTML = svg
            }
        })
    }, [code])

    return <div ref={ref} className="my-4 flex justify-center" />
}
