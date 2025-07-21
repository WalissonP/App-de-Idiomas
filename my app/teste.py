import flet as ft
from flet import (
    Page,
    Text,
    Column,
    Container,
    TextField,
    IconButton,
    icons,
    ElevatedButton,
    Divider,
    Ref,
    Row,
    alignment,
    ListView,
)
from dados import listar_idiomas, listar_palavras, adicionar_idioma, adicionar_palavra

idioma_selecionado = Ref[Text]()
campo_palavra = Ref[TextField]()
lista_palavras = Ref[ListView]()
total_palavras = Ref[Text]()

def main(page: Page):
    page.title = "App de Idiomas"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "AUTO"

    def carregar_idiomas():
        lista = listar_idiomas()
        idiomas_controls = []
        for idioma in lista:
            idiomas_controls.append(
                ft.TextButton(
                    content=ft.Text(idioma, size=16),
                    on_click=lambda e, i=idioma: selecionar_idioma(i),
                )
            )
        return idiomas_controls

    def selecionar_idioma(idioma):
        idioma_selecionado.current.value = idioma
        idioma_selecionado.current.update()
        mostrar_palavras()

    def mostrar_palavras():
        idioma = idioma_selecionado.current.value
        palavras = listar_palavras(idioma)
        lista_palavras.current.controls.clear()

        for palavra in palavras:
            lista_palavras.current.controls.append(
                ft.Text(palavra, size=16)
            )

        total_palavras.current.value = f"Total: {len(palavras)} palavras"
        total_palavras.current.update()
        lista_palavras.current.update()

    def adicionar_idioma_novo(e):
        def confirmar(e):
            nome_idioma = campo.value.strip()
            if nome_idioma:
                adicionar_idioma(nome_idioma)
                menu_idiomas.controls.insert(
                    -1,
                    ft.TextButton(
                        content=ft.Text(nome_idioma, size=16),
                        on_click=lambda e, i=nome_idioma: selecionar_idioma(i),
                    )
                )
                menu_idiomas.update()
                selecionar_idioma(nome_idioma)
            dlg.open = False
            page.update()

        campo = TextField(label="Novo idioma", autofocus=True)

        dlg = ft.AlertDialog(
            title=Text("Adicionar novo idioma"),
            content=campo,
            actions=[
                ElevatedButton("Adicionar", on_click=confirmar),
                ElevatedButton("Cancelar", on_click=lambda e: fechar_dialogo())
            ],
        )

        def fechar_dialogo():
            dlg.open = False
            page.update()

        page.dialog = dlg
        dlg.open = True
        page.update()

    def adicionar_nova_palavra(e):
        texto = campo_palavra.current.value.strip()
        idioma = idioma_selecionado.current.value

        if texto and idioma:
            adicionar_palavra(texto, idioma)
            campo_palavra.current.value = ""
            campo_palavra.current.update()
            mostrar_palavras()

    # Lateral esquerda: idiomas
    menu_idiomas = Column(
        controls=carregar_idiomas() + [
            Divider(),
            ft.TextButton("+ Adicionar novo idioma", on_click=adicionar_idioma_novo),
        ]
    )

    # Centro: palavras do idioma
    conteudo_principal = Column(
        spacing=10,
        controls=[
            Row(
                alignment="SPACE_BETWEEN",
                controls=[
                    Text(ref=idioma_selecionado, value="Selecione um idioma", size=24, weight="bold"),
                    IconButton(icon=icons.SETTINGS)
                ]
            ),
            Divider(),
            Row(
                alignment="SPACE_BETWEEN",
                controls=[
                    Text(ref=total_palavras, value="Total: 0 palavras", size=16, weight="bold"),
                    Row(
                        controls=[
                            TextField(ref=campo_palavra, hint_text="Nova palavra"),
                            IconButton(icon=icons.ADD, on_click=adicionar_nova_palavra),
                        ]
                    )
                ]
            ),
            Divider(),
            ListView(ref=lista_palavras, expand=True),
        ]
    )

    # Lateral direita: área da IA
    painel_chat = Column(
        controls=[
            Text("Chat com a IA (em breve)", size=18, weight="bold"),
            Divider(),
            Text("Área reservada para dúvidas com IA...", italic=True, size=14),
        ]
    )

    # Layout final
    page.add(
        Row(
            expand=True,
            spacing=10,
            controls=[
                Container(
                    width=220,
                    padding=10,
                    bgcolor=ft.colors.BLUE_GREY_700,
                    border_radius=10,
                    content=Column(
                        controls=[
                            Text("Idiomas", size=20, weight="bold"),
                            Divider(),
                            menu_idiomas,
                        ]
                    )
                ),
                Container(
                    expand=True,
                    padding=15,
                    bgcolor=ft.colors.BLUE_GREY_200,
                    border_radius=10,
                    content=conteudo_principal
                ),
                Container(
                    width=260,
                    padding=15,
                    bgcolor=ft.colors.BLUE_GREY_300,
                    border_radius=10,
                    content=painel_chat
                )
            ]
        )
    )

ft.app(target=main)
