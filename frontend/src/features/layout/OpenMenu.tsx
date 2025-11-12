// SPDX-FileCopyrightText: 2025 Weibo, Inc.
//
// SPDX-License-Identifier: Apache-2.0

'use client';

import { useState } from 'react';
import { ChevronDownIcon, ExternalLinkIcon } from '@heroicons/react/24/outline';

interface OpenMenuProps {
  gitUrl: string;
  gitRepo: string;
  branchName: string;
  className?: string;
}

export default function OpenMenu({
  gitUrl,
  gitRepo,
  branchName,
  className = '',
}: OpenMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  // Generate git URL
  const getGitUrl = () => {
    if (gitUrl.includes('github.com')) {
      return `${gitUrl}/tree/${branchName}`;
    }
    // For other git providers, construct a generic URL
    return `${gitUrl}/-/tree/${branchName}`;
  };

  // Generate VS Code URL
  const getVSCodeUrl = () => {
    if (gitUrl.includes('github.com')) {
      const repoPath = gitUrl.replace('https://github.com/', '');
      return `vscode://vscode.github/remotehub/${repoPath}?ref=${branchName}`;
    }
    // For other git providers, use generic VS Code remote URL
    return `vscode://vscode.remote/remoteRepository/${gitUrl}?ref=${branchName}`;
  };

  const handleGitOpen = () => {
    const url = getGitUrl();
    window.open(url, '_blank');
    setIsOpen(false);
  };

  const handleVSCodeOpen = () => {
    const url = getVSCodeUrl();
    window.open(url, '_blank');
    setIsOpen(false);
  };

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 px-3 py-2 rounded-lg bg-surface border border-border shadow-sm hover:bg-muted focus:outline-none focus:ring-2 focus:ring-primary/40 transition-all duration-200"
        title="打开选项"
      >
        <span className="text-sm text-text-primary">打开</span>
        <ChevronDownIcon
          className={`w-4 h-4 text-text-primary transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-1 w-48 bg-surface border border-border rounded-lg shadow-lg z-50">
          <div className="py-1">
            <button
              onClick={handleGitOpen}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-text-primary hover:bg-muted transition-colors duration-150"
            >
              <ExternalLinkIcon className="w-4 h-4" />
              <span>从 Git 打开</span>
            </button>
            <button
              onClick={handleVSCodeOpen}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-text-primary hover:bg-muted transition-colors duration-150"
            >
              <ExternalLinkIcon className="w-4 h-4" />
              <span>从 VSCode 打开</span>
            </button>
          </div>
        </div>
      )}

      {/* Close dropdown when clicking outside */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
}