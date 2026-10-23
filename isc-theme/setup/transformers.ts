import { defineMarkdownTransformer, defineTransformersSetup } from '@slidev/types'
import { mermaidThemes } from './mermaid-themes'

/**
 * Expands ```` ```mermaid {theme: '<name>'} ```` into a standard mermaid
 * diagram prefixed with a `%%{init}%%` directive. The fence itself is then
 * handled by Slidev's built-in mermaid renderer, so scale/options keep
 * working exactly as before.
 */
const expandMermaidTheme = defineMarkdownTransformer(({ s }) => {
  s.replace(/^```mermaid[ \t]*\{([^\n]*)\}[ \t]*$/gm, (fence, options: string) => {
    const name = options.match(/theme:\s*['"]([\w-]+)['"]/)?.[1]
    const theme = name && mermaidThemes[name]
    if (!theme)
      return fence

    // Drop only the custom theme key, keep the remaining options (e.g. scale).
    const rest = options
      .replace(/theme:\s*['"][\w-]+['"]\s*,?/, '')
      .replace(/,\s*$/, '')
      .trim()

    const open = rest ? `\`\`\`mermaid {${rest}}` : '```mermaid'
    return `${open}\n%%{init: ${JSON.stringify(theme)}}%%`
  })
})

export default defineTransformersSetup(() => ({
  pre: [expandMermaidTheme],
}))
