// @ts-check
import { defineConfig } from 'astro/config';
import { fileLinker } from './file-linker.mjs';

const FONTS_SOURCE = '../build/webfonts'
const FONTS_TARGET = './public/fonts'


// https://astro.build/config
export default defineConfig({
    integrations: [
        fileLinker(FONTS_SOURCE, FONTS_TARGET)
    ],
});
