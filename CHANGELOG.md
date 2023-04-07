# Changelog
All notable changes to this project will be documented in this file.

## 2.200 — Unreleased

## Fixed

* Long `----` and `====` are no longer breaking in iTerm2.
* Metrics (`underlineThickness`, `hhea`, `usWinAscent`, `usWinDescent`, `panose`).
* Width of some glyphs.
* `fsSelection` and `macStyle`.
* Arrows with `ss01`.
* `||` distance in arrows.

## Removed

* The `ccmp` feature is no longer available. The feature is too crude and will take time to refine.
* OTF is no longer available in the bundle. But you still have the option of building it yourself.

## Added

* `..=`, `#=`, `+=`, `^=`, `..<`, `#?`.
* `:::`, `;;`, `%%`, `>>>`, `<<<`, `+++`, `??`.
* `<>`, `|>`, `<|`, `<+>`, `||>`, `<||`, `|||`.
* `<$`, `$>`, `<$>`.
* Generated bar-underscores `_|_|_`.
* Powerline support (`uniE0A0`, `uniE0A2`, `uniE0B0`, `uniE0B1`, `uniE0B2`, `uniE0B3`).
* ExtraThick weight (Read [commit](https://github.com/mishamyrt/Lilex/commit/fe983370a278eca78a27434f2ddbf75e8505e8ed) message).
* Fontbakery reports to bundle.
* `ss02` for gap in equals (`==`, `!=`, `===`, `!==`).
* Greater/less colon vertical alignment.

## [2.100] — April 2, 2023

## Fixed

* `044B` (`ы`), `042B` (`Ы`) point order (In 400-700 the scaling was broken).
* Updated the clock arrows (`↺`, `↻`) to make them round. The original arrows are available in `cv07`.

## Added

* Medium and ExtraLight (they're back!)
* Arrows (and Markdown tables). `~>`, `<~`, `<~~`, `<~>`, `<<-|->>`, `<<=|=>> `, `|--|--|`
* Forced feature activation in the builder
* `<*`, `<*>`
* `{|`, `|}`, `|]`, `[|`, `<|>`

## [2.000] — March 28, 2023

## Removed

* Ugly `fl` and `fi`

## Added

* Generative `##` and `__` ligatures. Sequences of these characters can now be of any length

## Fixed

* `_` alignment

## [2.000-b1] — March 27, 2023

Based on IBM Plex Mono v6.0.0.

Font rebuilt from scratch, ligatures redrawn. Improved alignment of many characters.

## Added

* Thin weight (Now the weight range is from 100 to 700)
* Boxes
* `/**`

## Removed (At least for now)

* `www`
* `~=`

## [1.100] — November 21, 2020

Added `#{` `#[` `#(` `__(` `!!`

Improved `/*` `*/` `:=`

Slightly decreased width.

Migrated to Glyphs.

## [1.000] — October 25, 2019

Removed Retina, added Medium.

## [1.000-rc1] — October A21, 2019

Rebuilt from bash scripts to Makefile.

Added `##` `###` `####` `<=>` `>>` `=>>` `=:=` `=!=` `<<=` `/~\`.

Fixed arrows hinting.

Added colon vertical alignment in time sequences `10:22`.

## [1.000-b2] — October 16, 2019

Refused from using the patching method to create my own source code based on IBM Plex Mono.

Made a variable TTF.

Added `&&` `==` `===` `!=` `!==` `~~` `||` `**` `***` `//` `=>` `~~>` `>=` `<=` `*>` `/*` `*/` `.?` `~=` `--` `++` `..` `...` `::` `#!` `</` `/>` `www` `__` `/=` `.=` `:=` `->` `<-` `</>`.

## [1.000-b1] — October 9, 2019

Initial release:

Builded using monkey patching method.

Fira Code version: 2.000
IBM Plex Mono version: 3.000

[1.000-b1]: https://github.com/mishamyrt/Lilex/releases/tag/1.000-beta

[1.000-b2]: https://github.com/mishamyrt/Lilex/releases/tag/1.000-beta2

[1.000-rc1]: https://github.com/mishamyrt/Lilex/releases/tag/1.000-rc1

[1.000]: https://github.com/mishamyrt/Lilex/releases/tag/1.000

[1.100]: https://github.com/mishamyrt/Lilex/releases/tag/1.100

[2.000-b1]: https://github.com/mishamyrt/Lilex/releases/tag/2.000-b1

[2.000]: https://github.com/mishamyrt/Lilex/releases/tag/2.000

[2.100]: https://github.com/mishamyrt/Lilex/releases/tag/2.100
