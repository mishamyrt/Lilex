"""Font build results rich console renderable"""

import os

from rich.console import Group as RenderGroup
from rich.table import Table
from rich.text import Text

from .context import BuildContext
from .external_tools.fontmake import FontFormat


class FontBuildResult(RenderGroup):
    def __init__(self, result: list[list[BuildContext]], output_dir: str):
        output_by_format: dict[FontFormat, list[tuple[str, int]]] = {}
        for contexts_by_font in result:
            for context in contexts_by_font:
                if context.format not in output_by_format:
                    output_by_format[context.format] = []

                file_names = []
                file_sizes = []
                for file_path in context.artifacts["output_files"]:
                    file_names.append(os.path.basename(file_path))
                    file_sizes.append(int(os.path.getsize(file_path) / 1024))
                output_by_format[context.format].extend(
                    zip(file_names, file_sizes, strict=True)
                )

        format_outputs = sorted(output_by_format.items(), key=lambda x: x[0].value)
        output_count = 0
        for _, outputs in format_outputs:
            outputs.sort(key=lambda x: x[0])
            output_count += len(outputs)

        files_table = Table(box=None, pad_edge=False, show_header=False)
        files_table.add_column(justify="left")
        files_table.add_column(style="dim", no_wrap=True)

        for fmt, files in format_outputs:
            fmt_out_path = os.path.join(output_dir, fmt.value)
            for name, size in files:
                path = Text.assemble((f"{fmt_out_path}/", "dim"), (name, "cyan"))
                files_table.add_row(path, f"{size} KiB")

        super().__init__(
            Text(f"✓ {output_count} font binaries successfully built\n", style="green"),
            files_table,
        )
