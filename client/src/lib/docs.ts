const docs = import.meta.glob('../docs/*.md', {
    eager: true,
    query: '?raw',
    import: 'default',
})

export function getDoc(slug: string) {
    return docs[`../docs/${slug}.md`] as string | undefined
}

const h1Regex = /^#\s+(.+)$/m

export function getAllDocs() {
    return Object.entries(docs)
        .map(([path, content]) => {
            const slug = path.split('/').pop()?.replace('.md', '') ?? ''

            const match = h1Regex.exec(content as string)
            const title = match?.[1] ?? slug.replace(/-/g, ' ')

            return { slug, title }
        })
        .sort((a, b) =>
            a.title.localeCompare(b.title, undefined, {
                sensitivity: 'base',
            })
        )
}
