import math
import os
from pathlib import Path
from typing import Dict
from main import like_tweets

import flet as ft
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
from flet_core import Alignment, colors, theme
from dotenv import load_dotenv

# print(os.environ.get("FLET_SECRET_KEY"))
# load_dotenv(".env")
# print(os.environ.get("FLET_SECRET_KEY"))
def main(page: ft.Page):
    page.title = "my app"


    lv = ft.ListView(expand=1, spacing=10, padding=20)

    lv.controls.append(ft.Row([ft.Container(text_ := ft.Text("data"))], alignment=ft.MainAxisAlignment.SPACE_EVENLY, ))
    lv.controls.append(ft.Row([ft.Text("")], ))


    # page.add(ft.Row([], ))
    # page.add(ft.Row([], ))


    process_count = ft.TextField(label="threads count", disabled=True, value="1", text_align=ft.TextAlign.CENTER, )
    run_mode = ft.Dropdown(
        label="Run Mode", hint_text="Choose mode",
        options=[
            ft.dropdown.Option("Like by url file"),
            ft.dropdown.Option("Like by tag search"),
        ],
    )

    like_count = ft.TextField(label="likes count", value="2", text_align=ft.TextAlign.CENTER, )
    search_text = ft.TextField(label="search text", text_align=ft.TextAlign.CENTER, )
    timeout_between_like = ft.TextField(label="timeout between like", value="2", text_align=ft.TextAlign.CENTER, )
    timeout_between_account_change = ft.TextField(label="timeout between account change", value="2", text_align=ft.TextAlign.CENTER, )

    headless_checkbox = ft.Checkbox(label="headless: without browser showing", value=True)

    # file_of_link_path = ft.FilePicker("4")
    # accounts_file_path = ft.FilePicker(on_upload="4")
    # file_picker = ft.FilePicker()
    # page.overlay.append(file_picker)
    # page.update()

    prog_bars: dict[str, Dict[str, ProgressRing]] = {
        "proxy_file_picker": {},
        "login_file_picker": {},
        "links_file_picker": {}
    }

    proxy_file_picker_bar: Dict[str, ProgressRing] = {}
    login_file_picker_bar: Dict[str, ProgressRing] = {}
    links_file_picker_bar: Dict[str, ProgressRing] = {}

    files: dict[str, Ref[Column]] = {
        "proxy_file_picker": Ref[Column],
        "login_file_picker": Ref[Column],
        "links_file_picker": Ref[Column]
    }

    proxy_file_picker_files: Ref[Column] = Ref[Column]
    login_file_picker_files: Ref[Column] = Ref[Column]
    links_file_picker_files: Ref[Column] = Ref[Column]

    upload_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent, _files: Ref[Column], _prog_bars: Dict[str, ProgressRing]):
        # upload_button.current.disabled = True if e.files is None else False
        _prog_bars.clear()

        _files.current.controls.clear()

        if e.files is not None:
            for f in e.files:
                print(f"{e.path=} {f.path=}, {f.name=}")
                # print(f"{page.get_upload_url(f.name, 600)}")
                prog = ProgressRing(value=0, bgcolor="#eee", width=20, height=20)
                # _prog_bars[f.name] = prog
                _files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def file_picker_result_1(e: FilePickerResultEvent):

        page.update()
        # upload_button.current.disabled = True if e.files is None else False
        proxy_file_picker_bar.clear()

        proxy_file_picker_files.current.controls.clear()

        if e.files is not None:
            for f in e.files:
                print(f"{e.path=} {f.path=}, {f.name=}")
                # print(f"{page.get_upload_url(f.name, 600)}")
                prog = ProgressRing(value=0, bgcolor="#eee", width=20, height=20)
                proxy_file_picker_bar[f.name] = prog
                proxy_file_picker_files.current.controls.append(Row([prog, Text(f.name)]))
        files_added.value = (
            f"{proxy_file_picker_bar}" "\n"
            f"{login_file_picker_bar}" "\n"
            f"{links_file_picker_bar}" "\n"
        )
        page.update()

    def file_picker_result_2(e: FilePickerResultEvent):

        # upload_button.current.disabled = True if e.files is None else False
        login_file_picker_bar.clear()

        login_file_picker_files.current.controls.clear()

        if e.files is not None:
            for f in e.files:
                print(f"{e.path=} {f.path=}, {f.name=}")
                # print(f"{page.get_upload_url(f.name, 600)}")
                prog = ProgressRing(value=0, bgcolor="#eee", width=20, height=20)
                login_file_picker_bar[f.name] = prog
                login_file_picker_files.current.controls.append(Row([prog, Text(f.name)]))
        files_added.value = (
            f"{proxy_file_picker_bar}" "\n"
            f"{login_file_picker_bar}" "\n"
            f"{links_file_picker_bar}" "\n"
        )
        page.update()


    def file_picker_result_3(e: FilePickerResultEvent):


        # upload_button.current.disabled = True if e.files is None else False
        links_file_picker_bar.clear()

        links_file_picker_files.current.controls.clear()

        if e.files is not None:
            for f in e.files:
                print(f"{e.path=} {f.path=}, {f.name=}")
                # print(f"{page.get_upload_url(f.name, 600)}")
                prog = ProgressRing(value=0, bgcolor="#eee", width=20, height=20)
                links_file_picker_bar[f.name] = prog
                links_file_picker_files.current.controls.append(Row([prog, Text(f.name)]))

        files_added.value = (
            f"{proxy_file_picker_bar}" "\n"
            f"{login_file_picker_bar}" "\n"
            f"{links_file_picker_bar}" "\n"
        )
        page.update()

    def proxys_file_picker_result(e: FilePickerResultEvent):
        return file_picker_result_1(e)
        # return file_picker_result(e, proxy_file_picker_files, prog_bars["proxy_file_picker"])

    def logins_file_picker_result(e: FilePickerResultEvent):
        return file_picker_result_2(e)
#         return file_picker_result(e, login_file_picker_files, prog_bars["login_file_picker"])

    def links_file_picker_result(e: FilePickerResultEvent):
        return file_picker_result_3(e)
#         return file_picker_result(e, links_file_picker_files, prog_bars["links_file_picker"])

    def on_upload_progress(e: FilePickerUploadEvent):
        print("555555555555555555555555555555"*5)
        # prog_bars[e.file_name].value = e.progress
        # prog_bars[e.file_name].update()

    # file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)
    proxy_file_picker = FilePicker(on_result=file_picker_result_1, on_upload=on_upload_progress)
    login_file_picker = FilePicker(on_result=file_picker_result_2, on_upload=on_upload_progress)
    links_file_picker = FilePicker(on_result=file_picker_result_3, on_upload=on_upload_progress)

    # def upload_files(e):
    #     uf = []
    #     if file_picker.result is not None and file_picker.result.files is not None:
    #         for f in file_picker.result.files:
    #             # print("url: ", page.get_upload_url(f.name, 600))
    #             uf.append(
    #                 FilePickerUploadFile(
    #                     f.name,
    #                     upload_url=page.get_upload_url(f.name, 600),
    #                 )
    #             )
    #         file_picker.upload(uf)

    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )

    # hide dialog in an overlay
    # page.overlay.append(file_picker)
    page.overlay.append(proxy_file_picker)
    page.overlay.append(login_file_picker)
    page.overlay.append(links_file_picker)

    page.theme = ft.Theme(
        # color_scheme=ft.ColorScheme(
        #     primary=colors.GREEN,
        #     primary_container=colors.GREEN_200,
        #     secondary=colors.BLUE,
        #     # background=colors.RED,
        #
        # ),
        color_scheme_seed=colors.RED
    )

    # page.bgcolor = colors.DEEP_ORANGE_ACCENT_100

    # page.add(
    #     ft.Container(
    #         alignment=ft.alignment.center,
    #         gradient=ft.LinearGradient(
    #             begin=ft.alignment.top_left,
    #             end=Alignment(0.8, 1),
    #             colors=[
    #                 "0xff1f005c",
    #                 "0xff5b0060",
    #                 "0xff870160",
    #                 "0xffac255e",
    #                 "0xffca485c",
    #                 "0xffe16b5c",
    #                 "0xfff39060",
    #                 "0xffffb56b",
    #             ],
    #             tile_mode=ft.GradientTileMode.MIRROR,
    #             rotation=math.pi / 3,
    #         ),
    #         width=555,
    #         height=556,
    #         border_radius=5,
    #
    #     )
    # )

    lv.controls.append(
        ft.Column([
            # ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
            ft.Container(
                Row(
                    [ft.Container(content=process_count)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                Row(
                    [ft.Container(content=run_mode)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                Row(
                    [ft.Container(content=headless_checkbox)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                ft.Row(
                    [ft.Container(content=like_count)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                ft.Row(
                    [ft.Container(content=search_text)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                Row(
                    [ft.Container(content=timeout_between_like)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            ft.Container(
                Row(
                    [ft.Container(content=timeout_between_account_change)],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            ),
            # Row(ft.Container(bgcolor=colors.random_color(), content=[run_mode]), alignment=ft.MainAxisAlignment.CENTER)),
            # Row(ft.Container(bgcolor=colors.random_color(), content=[like_count]), alignment=ft.MainAxisAlignment.CENTER)),
            # Row(ft.Container(bgcolor=colors.random_color(), content=[timeout_between_like]), alignment=ft.MainAxisAlignment.CENTER)),
            # Row(ft.Container(bgcolor=colors.random_color(), content=[timeout_between_account_change]), alignment=ft.MainAxisAlignment.CENTER,)),
        ],
            # scroll=ft.ScrollMode.ALWAYS,
            # on_scroll=on_column_scroll,
            # expand=1,
        )

        # ft.Column([file_picker]),
        # ft.IconButton(ft.icons.ADD, on_click=plus_click),
    )

    lv.controls.append(
        ft.Container(ft.Row([files_added := ft.Text((
            f"{proxy_file_picker_bar}" "\n"
            f"{login_file_picker_bar}" "\n"
            f"{links_file_picker_bar}" "\n")
        )])),
    )



    # lv.update()

    lv.controls.append(
        ft.Container(ft.Column([
            # ft.Row([
            #     ft.Text("File"),
            #     Column(ref=files),
            #     ElevatedButton(
            #         "open",
            #         icon=icons.FILE_OPEN_ROUNDED,
            #         on_click=lambda _: file_picker.pick_files(allow_multiple=True),
            #     ),
            #     # Column(ref=files),
            #     # ElevatedButton(
            #     #     "Upload",
            #     #     ref=upload_button,
            #     #     icon=icons.UPLOAD,
            #     #     on_click=upload_files,
            #     #     disabled=True,
            #     # )
            # ],
            #     alignment=ft.MainAxisAlignment.CENTER
            #     # scroll=ft.ScrollMode.ALWAYS,
            #     # expand=1,
            #     # vertical_alignment=ft.CrossAxisAlignment.START
            # ),
            # ft.Container(ft.Row([Column(ref=proxy_file_picker_files), Column(ref=login_file_picker_files), Column(ref=links_file_picker_files),])),

            ft.Column([
                ft.Container(ft.Row([
                    ft.Text("Proxys File"),
                    Column(ref=proxy_file_picker_files),
                    ElevatedButton(
                        "open",
                        icon=icons.FILE_OPEN_ROUNDED,
                        on_click=lambda _: proxy_file_picker.pick_files(allow_multiple=True),
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                ))
                ]),
            ft.Column([
                ft.Container(ft.Row([
                    ft.Text("Logins File"),
                    Column(ref=login_file_picker_files),
                    ElevatedButton(
                        "open",
                        icon=icons.FILE_OPEN_ROUNDED,
                        on_click=lambda _: login_file_picker.pick_files(allow_multiple=True),
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                ))
                ]),
            ft.Column([
                ft.Container(ft.Row([
                    ft.Text("Links File"),
                    Column(ref=links_file_picker_files),
                    ElevatedButton(
                        "open",
                        icon=icons.FILE_OPEN_ROUNDED,
                        on_click=lambda _: links_file_picker.pick_files(allow_multiple=True),
                    ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                )),
            ])
        ])),
    )


    # page.theme = ft.Theme(
    #     color_scheme=ft.ColorScheme(
    #         primary=colors.GREEN,
    #         primary_container=colors.GREEN_200
    #     )
    # )

    def btn_click(e):
        data = (
            f"{'data_value'.upper()}: " "\n"
            f"{process_count=},{type(process_count)=}, " "\n"
            f"{run_mode=}, " "\n"
            f"{like_count=}, " "\n"
            f"{timeout_between_like=}, " "\n"
            f"{timeout_between_account_change=}, " "\n"
            f"{prog_bars=}, " "\n"
            f"{files=}" "\n"
        )
        # print(data)

        data_value = (
            f"{'data_value'.upper()}: " "\n"
            f"{process_count.value=}, " "\n"
            f"{run_mode.value=}, " "\n"
            f"{like_count.value=}, " "\n"
            f"{timeout_between_like.value=}, " "\n"
            f"{timeout_between_account_change.value=}, " "\n"
            f"{prog_bars=}, " "\n"
            # f"{files=}" "\n"
            f"{proxy_file_picker.result.files[0].path=}" "\n"
            f"{proxy_file_picker_files=}" "\n"
            f"{login_file_picker.result.files[0].path=}" "\n"
            f"{login_file_picker_files=}" "\n"
            f"{links_file_picker.result.files[0].path=}" "\n"
            f"{links_file_picker_files=}" "\n"
            # f"{page.get_upload_url(files, 600)}"
        )
        print(data_value)

        data_data = (
            f"{'data_data'.upper()}: "
            f"{process_count.data}, "
            f"{run_mode.data}, "
            f"{like_count.data}, "
            f"{timeout_between_like.data}, "
            f"{timeout_between_account_change.data}, "
            f"{prog_bars}, "
            f"{files}"
        )
        # print(data_data)

        # text_.value = data_value

        like_tweets(
            mode="link" if run_mode.value == "Like by url file" else "latest_posts" if run_mode.value == "Like by tag search" else "",
            likes_count=int(like_count.value),
            threads_count=int(process_count.value),
            links_file=links_file_picker.result.files[0].path,
            login_data=login_file_picker.result.files[0].path,
            proxy_data=proxy_file_picker.result.files[0].path,
            timeout=int(timeout_between_like.value),
            timeout_accounts=int(timeout_between_account_change.value),
            path_to_chromedriver=None,
            text_to_search=search_text.value,
            headless=headless_checkbox.value
        )




        page.update()

    lv.controls.append(
        ft.Row(
            [ft.TextButton("run", on_click=btn_click)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    page.add(lv)

    # page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = theme.Theme(color_scheme_seed=colors.random_color())

    # page.add(ft.Container(cl, border=ft.border.all(1)),)

    page.update()

    # page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


ft.app(main, upload_dir="ui")
