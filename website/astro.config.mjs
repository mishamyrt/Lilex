// @ts-check
import { defineConfig } from "astro/config";
import { fileLinker } from "./file-linker.mjs";
import typograf from "astro-typograf";

const FONTS_SOURCE = "../build/Lilex/webfonts";
const FONTS_TARGET = "./public/fonts";

// https://astro.build/config
export default defineConfig({
  integrations: [
    fileLinker(FONTS_SOURCE, FONTS_TARGET),
    typograf({
      selector: "p",
      typografOptions: {
        locale: ["en-US"],
        htmlEntity: { type: "name" },
      },
    }),
  ],
});
