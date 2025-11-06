// @ts-check

import { execSync } from "node:child_process";
import { existsSync, statSync } from "node:fs";

/**
 * Create a file linker integration for Astro
 *
 * It will create a symlink to the source directory in the target directory.
 *
 * @param {string} source source directory or file
 * @param {string} target target directory or file
 * @returns {import('astro').AstroIntegration}
 */
export function fileLinker(source, target) {
  if (!existsSync(source)) {
    console.warn(`[fileLinker] Source ${source} does not exist`);
    return {
      name: "fileLinker",
      hooks: {
        "astro:server:setup": () => {},
      },
    };
  }

  const createSymlink = statSync(source).isDirectory()
    ? createDirectoryLinker(source, target)
    : createFileLinker(source, target);

  return {
    name: "fileLinker",
    hooks: {
      "astro:build:setup": createSymlink,
      "astro:server:setup": createSymlink,
    },
  };
}

/**
 * Create a file linker function
 *
 * @param {string} source source file
 * @param {string} target target file
 * @returns {() => void}
 */
function createFileLinker(source, target) {
  return () => {
    execSync(`rm -f "${target}"`);
    execSync(`ln "${source}" "${target}"`);
  };
}

/**
 * Create a directory linker function
 *
 * @param {string} source source directory
 * @param {string} target target directory
 * @returns {() => void}
 */
function createDirectoryLinker(source, target) {
  return () => {
    execSync(`rm -rf "${target}"`);
    execSync(`mkdir "${target}"`);
    execSync(`ln "${source}"/* "${target}"`);
  };
}
