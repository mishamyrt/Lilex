// @ts-check
import { defineConfig } from "astro/config";
import { fileLinker } from "./file-linker.mjs";
import typograf from "astro-typograf";

const BUILD_DIR = "../build";

const FONTS_SOURCES = [
  `${BUILD_DIR}/LilexDuo/webfonts/LilexDuo\\[wght\\].woff2`,
  `${BUILD_DIR}/Lilex/webfonts/Lilex*\\[wght\\].woff2`,
];
const FONTS_TARGET = "./public/fonts";
// https://astro.build/config
export default defineConfig({
  integrations: [
    fileLinker(FONTS_SOURCES, FONTS_TARGET),
    typograf({
      selector: "p",
      typografOptions: {
        locale: ["en-US"],
        htmlEntity: { type: "name" },
      },
    }),
  ],
});
