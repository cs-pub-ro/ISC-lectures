/**
 * Named Mermaid themes for this Slidev theme.
 *
 * Mermaid's `theme` option only accepts its built-in names, so a "theme" here
 * is a plain Mermaid config preset. `setup/transformers.ts` expands
 * `{theme: '<name>'}` inside a mermaid fence into the equivalent
 * `%%{init: { ... }}%%` directive, which Mermaid applies per diagram.
 *
 * Usage:
 *
 *   ```mermaid {theme: 'isc-cartoon', scale: 0.65}
 *   flowchart LR
 *     A --> B
 *   ```
 */
export const mermaidThemes: Record<string, Record<string, unknown>> = {
  // White fill, thick black rounded borders, pill edge labels.
  'isc-cartoon': {
    theme: 'base',
    themeVariables: {
      background: '#ffffff',
      primaryColor: '#ffffff',
      primaryBorderColor: '#000000',
      primaryTextColor: '#000000',
      lineColor: '#000000',
      edgeLabelBackground: '#ffffff',
      tertiaryColor: '#ffffff',
      fontSize: '15px',
    },
    themeCSS: [
      '.node rect,.node polygon,.node circle{fill:#fff !important;stroke:#000 !important;stroke-width:4px !important}',
      '.node rect{rx:14px;ry:14px}',
      '.nodeLabel,.nodeLabel p{color:#000 !important;font-weight:600 !important}',
      '.nodeLabel em,.nodeLabel i{font-style:italic !important;font-weight:400 !important}',
      '.edgePath path{stroke:#000 !important;stroke-width:3px !important}',
      'marker path,.marker path{fill:#000 !important;stroke:#000 !important}',
      '.labelBkg p{background:#fff !important;color:#000 !important;font-weight:700 !important;font-size:14px !important;padding:1px 8px !important;border:2px solid #000;border-radius:10px;margin:0 !important}',
    ].join(''),
  },
}
