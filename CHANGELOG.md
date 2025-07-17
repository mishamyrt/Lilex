# Changelog
All notable changes to this project will be documented in this file.

## Next

### Added

* Italic denominators. (`dnom`)

### Fixed

* Remove overlaps from half black circles. (`◖`, `◗`)
* Greek capital letters with Tonos alignment in italic. (`Ά`, `Έ`, `Ή`, `Ί`, `Ό`, `Ύ`, `Ώ`)

### Removed

* Unreachable glyphs (`IJacute`, `ijacute`).
* Soft hyphen.

## [2.601] — July 16, 2025

### Fixed

* The font now shows the correct version corresponding to the current release (not n-1).

## [2.600] — September 25, 2024

### Added

* Italic variant.
* Cyrillic yus (`ѫ`, `Ѫ`).
* Spaces. (enspace, emspace, enquad, emquad, threeperemspace, fourperemspace, sixperemspace, figurespace, thinspace, mediumspace-math)
* Replacement glyph. (`�`)
* Cedi glyph. (`₵`)
* Guarani glyph. (`₲`)

### Fixed

* Bar-hyphen alignment. (`||-`)

## [2.530] — July 27, 2024

### Added

* Circles. (`●`, `○◯`, `◐◑◒◓`, `◖◗`, `◔`, `◜◝◟◞`)

### Changed

* Replaced the `ß` glyph, the previous version is available under the `cv12` variant.

## [2.520] — July 19, 2024

### Fixed

* Combs alignment. (`ỐỔỖǪǫ`, `Ḩḩ`, `ẲẴẤẨẢ`, `ỂỄ`)
* Variable "Thin" variant.
* Variable tables.

### Removed

* ExtraThick variant. This is a non-standard variant that doesn't pass Google Fonts checks. If you want to get this typeface, take a variable font and give it a weight of 450.

## [2.510] — May 10, 2024

### Added

* One storey alpha. (`α`, `ά`)

### Fixed

* Variable font interpolation problems for some glyphs.

### Removed

* Some unreachable glyphs.

## [2.500] — May 9, 2024

### Added

* [Power symbols](https://unicodepowersymbol.com/).
* Pre-1918 missing cyrillic. (`Ѣѣ`, `Ѵѵ`)
* Math ratio symbol. (`uni2236`)
* Bullet operator symbol. (`∙`)
* Dashes. (`uni2010`—`uni2015`)
* Spaces. (`uni2028`, `uni2029`, `uni202F`, `uni2008`, `uni200A`, `uni200B`)
* Abkhazian cyrillic letters. (`Ӷӷ`, `Ӡӡ`, `Ҟҟ`, `Ԥԥ`, `Ҧҧ`, `Ҭҭ`, `Ҵҵ`, `Ҽҽ`, `Ҿҿ`, `Ҩҩ`)
* Old-style numerals. (`onum`)
* Bulgarian localized forms.

### Fixed

* No more arrows breaking on Windows with TTF.
* Greek support.

### Improved

* Subpixel equal combinations shifts in small sizes.
* Shapes for cyrillic fita. (`Ѳ`, `ѳ`)
* Shapes for cyrillic es with descender. (`Ҫ`, `ҫ`)

## [2.400] — December 17, 2023

### Added

* `ss04` for broken number signs. (`####`) [#28](https://github.com/mishamyrt/Lilex/pull/28)
* `(*`, `*)`.

### Fixed

* Aligning slash asterisk sequences. (`/*`, `*/`) [#29](https://github.com/mishamyrt/Lilex/pull/29)

## [2.300] — November 7, 2023

### Added

* `cv11` for connected bar with less or greater. (`<|`, `|>`)

### Fixed

* `Medium` naming.
* Vertical align for some arrow parts. (`greater_greater_equal_end.seq`, `greater_greater_equal_middle.seq`)

## [2.200] — April 13, 2023

### Fixed

* Long `----` and `====` are no longer breaking in iTerm2.
* Metrics. (`underlineThickness`, `hhea`, `usWinAscent`, `usWinDescent`, `panose`)
* Width of some glyphs.
* `fsSelection` and `macStyle`.
* Arrows with `ss01`.
* `||` distance in arrows.

### Removed

* OTF is no longer available in the bundle. But you still have the option of building it yourself.

### Added

* `..=`, `#=`, `+=`, `^=`, `..<`, `#?`.
* `:::`, `;;`, `%%`, `>>>`, `<<<`, `+++`, `??`.
* `<>`, `|>`, `<|`, `<+>`, `||>`, `<||`, `|||`.
* `<$`, `$>`, `<$>`.
* Generated bar-underscores `_|_|_`.
* Powerline support. (`uniE0A0`, `uniE0A2`, `uniE0B0`, `uniE0B1`, `uniE0B2`, `uniE0B3`)
* ExtraThick weight (Read [commit](https://github.com/mishamyrt/Lilex/commit/fe983370a278eca78a27434f2ddbf75e8505e8ed) message).
* Fontbakery reports to bundle.
* `ss02` for gap in equals (`==`, `!=`, `===`, `!==`).
* `cv08` for classical `>=`, `<=` with horizontal bar.
* `cv09` for barless `$` and `¢`.
* `cv10` for top–aligned `*`.
* Greater/less colon vertical alignment.

## [2.100] — April 2, 2023

### Fixed

* `044B` (`ы`), `042B` (`Ы`) point order (In 400-700 the scaling was broken).
* Updated the clock arrows (`↺`, `↻`) to make them round. The original arrows are available in `cv07`.

### Added

* Medium and ExtraLight (they're back!)
* Arrows (and Markdown tables). `~>`, `<~`, `<~~`, `<~>`, `<<-|->>`, `<<=|=>> `, `|--|--|`
* Forced feature activation in the builder
* `<*`, `<*>`
* `{|`, `|}`, `|]`, `[|`, `<|>`

## [2.000] — March 28, 2023

### Removed

* Ugly `fl` and `fi`

### Added

* Generative `##` and `__` ligatures. Sequences of these characters can now be of any length

### Fixed

* `_` alignment

## [2.000-b1] — March 27, 2023

Based on IBM Plex Mono v6.0.0.

Font rebuilt from scratch, ligatures redrawn. Improved alignment of many characters.

### Added

* Thin weight (Now the weight range is from 100 to 700)
* Boxes
* `/**`

### Removed (At least for now)

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

[2.200]: https://github.com/mishamyrt/Lilex/releases/tag/2.200

[2.300]: https://github.com/mishamyrt/Lilex/releases/tag/2.300

[2.400]: https://github.com/mishamyrt/Lilex/releases/tag/2.400

[2.500]: https://github.com/mishamyrt/Lilex/releases/tag/2.500

[2.510]: https://github.com/mishamyrt/Lilex/releases/tag/2.510

[2.520]: https://github.com/mishamyrt/Lilex/releases/tag/2.520

[2.530]: https://github.com/mishamyrt/Lilex/releases/tag/2.530

[2.600]: https://github.com/mishamyrt/Lilex/releases/tag/2.600

[2.601]: https://github.com/mishamyrt/Lilex/releases/tag/2.601
