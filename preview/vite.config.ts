import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { execSync } from 'child_process'
import { viteSingleFile } from "vite-plugin-singlefile"

const FONTS_SOURCE = '../build'
const FONTS_TARGET = './public'

function lnFontDir(format: string) {
    const sourcePath = `${FONTS_SOURCE}/${format}`
    const targetPath = `${FONTS_TARGET}/${format}`

    execSync(`rm -rf "${targetPath}"`)
    execSync(`mkdir "${targetPath}"`)
    execSync(`ln "${sourcePath}"/* "${targetPath}"`)
}

// https://vitejs.dev/config/
export default defineConfig(() => {
    lnFontDir('otf')
    lnFontDir('variable')
    return {
        plugins: [svelte(), viteSingleFile()],
    }
})
