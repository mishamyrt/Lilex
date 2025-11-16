// @ts-check

import path from "node:path";
import { unlink, rmdir, mkdir, link } from "node:fs/promises";
import { existsSync } from "node:fs";
import glob from "fast-glob";
/**
 * Create a file linker integration for Astro
 *
 * It will create a link to the source files in the target directory.
 *
 * @param {string[]} paths paths to source files. It can be a glob pattern.
 * @param {string} targetDir target directory
 * @returns {import('astro').AstroIntegration}
 */
export function fileLinker(paths, targetDir) {
  const sources = glob.sync(paths);
  const missing = sources.filter((source) => !existsSync(source));
  if (missing.length > 0) {
    console.error(
      `[fileLinker] Sources ${missing.join(", ")} do not exist. Skipping linking...`,
    );
    return {
      name: "fileLinker",
      hooks: {
        "astro:server:setup": () => {},
      },
    };
  }

  const createSymlinks = async () => {
    if (existsSync(targetDir)) {
      await rmdir(targetDir, { recursive: true });
    }
    await mkdir(targetDir, { recursive: true });
    const targets = sources.map((source) => linkFile(source, targetDir));
    await Promise.all(targets);
  };

  return {
    name: "fileLinker",
    hooks: {
      "astro:build:setup": createSymlinks,
      "astro:server:setup": createSymlinks,
    },
  };
}

/**
 * Creates a symlink to a file in a directory
 *
 * @param {string} source source file
 * @param {string} targetDir target directory
 * @returns {Promise<void>}
 */
async function linkFile(source, targetDir) {
  const target = path.join(targetDir, path.basename(source));
  if (existsSync(target)) {
    await unlink(target);
  }
  await link(source, target);
}
