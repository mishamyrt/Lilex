// @ts-check

import { join } from "node:path";
import { readdir, writeFile, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { exit } from "node:process";

/**
 * Create an OpenType feature collector for Astro
 *
 * Collects `.fea` files in the given directory.
 *
 * @param {string} path Path to the directory containing `.fea` files.
 * @param {string} target Path to the target json file where features will be collected.
 * @param {string[]} [ignore=[]] List of feature names to ignore.
 * @returns {import('astro').AstroIntegration}
 */
export function featureCollector(path, target, ignore = []) {
  if (!existsSync(path)) {
    console.error(
      `[fileLinker] Feature directory ${path} does not exist. Skipping...`,
    );
    exit(1);
  }

  const collectFeatures = async () => {
    const files = await readdir(path);
    const features = [];
    for (const fileName of files) {
      if (fileName.endsWith(".fea") && !ignore.some((i) => fileName.startsWith(i))) {
        const content = await readFile(join(path, fileName), "utf-8");
        const name = extractName(content);
        const code = fileName.substring(0, fileName.length - 4); // remove .fea extension
        features.push({ name, code });
      }
    }
    await writeFile(target, JSON.stringify(features));
    console.log(`Wrote ${features.length} features to ${target}`);
  };

  return {
    name: "fileLinker",
    hooks: {
      "astro:build:setup": collectFeatures,
      "astro:server:setup": collectFeatures,
    },
  };
}

/**
 * Extracts the name from the first line of a file content.
 *
 * @param {string} content file content
 * @returns {string} name extracted from the first line
 */
function extractName(content) {
  const lineEnd = content.indexOf("\n");
  const line = lineEnd === -1 ? content : content.substring(0, lineEnd);
  return line.replace("# Name: ", "").trim();
}
