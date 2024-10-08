// @ts-check

import { execSync } from "node:child_process"

/**
 * 
 * @param {string} sourceDir 
 * @param {string} targetDir
 * @returns {import('astro').AstroIntegration}
 */
export function fileLinker(sourceDir, targetDir) {
    const linkFiles = () => {
        execSync(`rm -rf "${targetDir}"`)
        execSync(`mkdir "${targetDir}"`)
        execSync(`ln "${sourceDir}"/* "${targetDir}"`)
    }

    return {
        name: 'fileLinker',
        hooks: {
            'astro:build:setup': linkFiles,
            'astro:server:setup': linkFiles
        }
    }
}
