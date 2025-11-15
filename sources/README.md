# Lilex Sources

This directory contains the source files for the Lilex font family. Source files heavily rely on [`lilexgen`](../scripts/lilexgen) library and code generation. The generation parameters are described in the [`lilexgen_config.yaml`](./lilexgen_config.yaml) file.


Generation is used to update the source files:

- Inject OpenType features from `.fea` and `.cls` files
- Generate `calt` feature based on glyphs
- Generate spacers for ligatures
- Clean up and normalize file.

Glyphs.app often changes line formatting (adds or removes quotation marks) and changes the internal order of fields. To improve the readability of git diff and remove clutter, the source code is regenerated before committing. This is done by running `make generate` command.

## Lilex

The process of working on Lilex monospaced font is as follows:

1. Change `.glyphs` files in [`Lilex/`](Lilex) directory
2. Save edited files
3. Run `make generate` to update the source code.
4. Run `make build-mono` to build the font
5. Run `make check-mono` to check the font quality.

## Lilex Duo

Lilex Duo is built as a patch based on Lilex. To do this, first the source `Lilex/Lilex.glyphs` is generated, then `LilexDuo/LilexDuo.patch.glyphs` is applied to it, resulting in `LilexDuo/LilexDuo.glyphs`.

> **Important**: It is important to NEVER EDIT `LilexDuo/LilexDuo.glyphs` manually. If you do so, the changes will be erased during the next generation.

The process of working on a font is as follows:

1. Change `.patch.glyphs` files in [`LilexDuo/`](LilexDuo) directory
2. Save edited files
3. Run `make generate` to update the source code.
4. Run `make build-duo` to build the font
5. Run `make check-duo` to check the font quality.
