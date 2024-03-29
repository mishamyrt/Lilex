import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { execSync } from 'child_process'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { resolve } from 'path'

const FONTS_SOURCE = '../build'
const FONTS_TARGET = './public'

function lnFontDir (format: string) {
  const sourcePath = `${FONTS_SOURCE}/${format}`
  const targetPath = `${FONTS_TARGET}/${format}`

  execSync(`rm -rf "${targetPath}"`)
  execSync(`mkdir "${targetPath}"`)
  execSync(`ln "${sourcePath}"/* "${targetPath}"`)
}

// https://vitejs.dev/config/
export default defineConfig(() => {
  lnFontDir('ttf')
  lnFontDir('variable')
  return {
    base: '',
    plugins: [svelte(), viteSingleFile()],
    resolve: {
      alias: {
        $components: resolve(__dirname, 'src/components'),
        $utils: resolve(__dirname, 'src/utils')
      }
    }
  }
})
