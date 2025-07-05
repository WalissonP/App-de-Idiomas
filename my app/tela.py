# Importações necessárias
import flet as ft
from dados import *  # Suas funções de CRUD

# Referências
idioma_atual = ft.Ref[ft.Text]()
lista_palavras = ft.Ref[ft.Column]()
nova_palavra = ft.Ref[ft.TextField]()
ft_ref_menu = ft.Ref[ft.Container]()

# Função principal
def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO  # Habilita scroll quando necessário
    page.title = "App de Idiomas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ----- Funções de login -----
    valido = read()
    nome_login = ft.TextField(label="Usuário", width=300)
    senha_login = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)
    mensagem_erro = ft.Text("Usuário ou senha incorretos!", color=ft.Colors.RED, visible=False)

    def validacao_login(e):
        for conta in valido:
            if nome_login.value in conta and senha_login.value in conta:
                mensagem_erro.visible = False
                ir_para_tela_principal()
                return
        senha_login.value = ""
        mensagem_erro.visible = True
        nome_login.focus()
        page.update()

    def cadastro():
        ...

    def go_to_register(e):
        page.views.append(register_view())
        page.update()

    def back_to_login(e):
        page.views.pop()
        page.update()

    def login():
        return ft.View(
            "/login",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Text("Login", size=30, weight="bold"),
                            nome_login,
                            senha_login,
                            mensagem_erro,
                            ft.ElevatedButton("Entrar", on_click=validacao_login),
                            ft.TextButton("Ainda não tem uma conta? Cadastre-se", on_click=go_to_register),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            ]
        )

    def register_view():
        return ft.View(
            "/register",
            controls=[
                ft.Text("Cadastre-se", size=30, weight="bold"),
                ft.TextField(label="Nome de usuário", width=300),
                ft.TextField(label="E-mail", width=300),
                ft.TextField(label="Senha (mínimo 6 dígitos)", password=True, can_reveal_password=True, width=300),
                ft.TextField(label="Confirmar senha", password=True, can_reveal_password=True, width=300),
                ft.ElevatedButton("Criar conta", on_click=cadastro),
                ft.TextButton("Já tem uma conta? Voltar para Login", on_click=back_to_login)
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # ----- Funções da tela principal -----
    def selecionar_idioma(e):
        idioma = e.control.data
        idioma_atual.current.value = f"Minhas palavras em {idioma}"
        page.update()

    def adicionar_palavra(e=None):
        texto = nova_palavra.current.value.strip()
        if texto:
            lista_palavras.current.controls.append(ft.Text(f"• {texto}"))
            nova_palavra.current.value = ""
            page.update()

    # Menu lateral fixo e responsivo
    menu_lateral = ft.Container(
        bgcolor=ft.Colors.BLUE_GREY,
        width=220,
        padding=20,
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_900),
        content=ft.Column(
            expand=True,
            spacing=10,
            controls=[
                ft.Row([
                    ft.Text("Idiomas", size=22, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE)
                ]),
                ft.TextButton("Inglês", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("Espanhol", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("Francês", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.Divider(color=ft.Colors.WHITE),
                ft.TextButton("+ Adicionar novo idioma", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.Container(expand=True),
            ]
        )
    )

    nova_palavra = ft.TextField(label="Nova palavra")
    lista_palavras = ft.Column(spacing=5)

    conteudo = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            expand=True,
            spacing=25,
            controls=[
                ft.Row([
                    ft.Text("Minhas palavras em Inglês", size=24, weight="bold"),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.BLUE_GREY),
                    ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.BLUE_GREY)
                ]),
                ft.Row(
                    expand=True,
                    spacing=30,
                    controls=[
                        ft.Container(
                            expand=2,
                            bgcolor=ft.Colors.BLUE_GREY_200,
                            border_radius=12,
                            padding=20,
                            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_100, offset=ft.Offset(2, 2)),
                            content=ft.Column([
                                ft.Text("Total: 0 palavras", size=18, weight="bold", color=ft.Colors.BLACK),
                                lista_palavras
                            ])
                        ),
                        ft.Container(
                            expand=1,
                            bgcolor=ft.Colors.BLUE_GREY_200,
                            border_radius=12,
                            padding=20,
                            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_100, offset=ft.Offset(2, 2)),
                            content=ft.Column([
                                ft.Text("Adicionar nova palavra", color=ft.Colors.BLACK, size=18, weight="bold"),
                                nova_palavra,
                                ft.ElevatedButton("Adicionar", color=ft.Colors.GREY_100,icon=ft.Icons.ADD, on_click=adicionar_palavra)
                            ])
                        )
                    ]
                )
            ]
        )
    )


    # Tela principal
    def ir_para_tela_principal():
        page.views.append(
            ft.View(
                route="/principal",
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        content=ft.Row(
                            expand=True,
                            spacing=0,
                            controls=[
                                menu_lateral,
                                conteudo
                            ]
                        )
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            )
        )
        page.go("/principal")


    # Adiciona view inicial (login)
    page.views.append(login())
    page.update()

# Executa o app
ft.app(target=main)
