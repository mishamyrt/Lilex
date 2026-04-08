// @ts-check
import { defineConfig } from "astro/config";
import { fileLinker } from "./file-linker.mjs";
import { featureCollector } from "./feature-collector.mjs";
import typograf from "astro-typograf";

const BUILD_DIR = "../build";

// https://astro.build/config
export default defineConfig({
  integrations: [
    fileLinker(
      [
        `${BUILD_DIR}/LilexDuo/webfonts/LilexDuo\\[wght\\].woff2`,
        `${BUILD_DIR}/Lilex/webfonts/Lilex*\\[wght\\].woff2`,
      ],
      "./public/fonts",
    ),
    featureCollector(
      "../sources/opentype_features",
      "./public/opentype_features.json",
      ["calt", "aalt", "locl"],
    ),
    typograf({
      selector: "p",
      typografOptions: {
        locale: ["en-US"],
        htmlEntity: { type: "name" },
      },
    }),
  ],
});
