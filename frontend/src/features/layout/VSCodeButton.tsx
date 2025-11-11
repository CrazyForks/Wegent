// SPDX-FileCopyrightText: 2025 Weibo, Inc.
//
// SPDX-License-Identifier: Apache-2.0

'use client'

import { Button } from 'antd'
import { useTranslation } from '@/hooks/useTranslation'

type VSCodeButtonProps = {
  className?: string
}

export function VSCodeButton({ className = '' }: VSCodeButtonProps) {
  const { t } = useTranslation('common')

  const mergedClassName = `
    px-3 py-1.5 rounded-full border border-transparent
    flex items-center gap-2 text-base font-semibold text-text-primary
    hover:border-border transition-colors duration-200
    ${className}
  `.trim()

  const handleOpenInVSCode = () => {
    // Open the current repository in VSCode using the vscode:// protocol
    const currentUrl = window.location.href
    const repoUrl = 'https://github.com/wecode-ai/Wegent'

    // Convert GitHub URL to VSCode protocol
    const vscodeUrl = `vscode://vscode.git/clone?url=${encodeURIComponent(repoUrl)}`

    try {
      window.open(vscodeUrl, '_blank')
    } catch (error) {
      // Fallback: open the GitHub repo in a new tab
      window.open(repoUrl, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <button
      type="button"
      onClick={handleOpenInVSCode}
      className={mergedClassName}
      aria-label="Open in VSCode"
      title="Open in VSCode"
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4"
        aria-hidden="true"
      >
        <path
          d="M8.5 1.5L2.5 5.5V10.5L8.5 14.5L14.5 10.5V5.5L8.5 1.5Z"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M2.5 5.5L8.5 9.5L14.5 5.5"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M8.5 14.5V9.5"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <span>VSCode</span>
    </button>
  )
}