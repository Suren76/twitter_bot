from typing import Dict

import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
)


def main(page: Page):
    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)

    # hide dialog in a overlay
    page.overlay.append(file_picker)

    page.add(
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),
    )
    prog_bars_second: Dict[str, ProgressRing] = {}
    files_second = Ref[Column]()
    upload_button_second = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent):
        upload_button_second.current.disabled = True if e.files is None else False
        prog_bars_second.clear()
        files_second.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog_second = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars_second[f.name] = prog_second
                files.current.controls.append(Row([prog_second, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars_second[e.file_name].value = e.progress
        prog_bars_second[e.file_name].update()

    file_picker_second = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []
        if file_picker_second.result is not None and file_picker_second.result.files is not None:
            for f in file_picker_second.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker_second.upload(uf)

    # hide dialog in a overlay
    page.overlay.append(file_picker_second)

    var = (
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),
    )

    page.add(*var)

    page.add(
        ElevatedButton(
            "Select files _second...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker_second.pick_files(allow_multiple=True),
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload _second",
            ref=upload_button_second,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),
    )


flet.app(target=main, upload_dir="./uploads")
