import flet as ft
from dados import *

# Referências globais
idioma_atual = ft.Ref[ft.Text]()
lista_palavras = ft.Ref[ft.Column]()
nova_palavra = ft.Ref[ft.TextField]()
menu_idiomas = ft.Ref[ft.Column]()
mostrar_input_idioma = ft.Ref[ft.Container]()
input_novo_idioma = ft.Ref[ft.TextField]()
lista_idiomas = ft.Ref[ft.Column]()
mostrar_input = ft.Ref[ft.Container]()
campo_idioma = ft.Ref[ft.TextField]()

# Função principal
def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    page.title = "App de Idiomas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Login e Cadastro -------------------------------
    valido = read()
    nome_login = ft.TextField(label="Usuário", width=300)
    senha_login = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)
    mensagem_erro = ft.Text("Usuário ou senha incorretos!", color=ft.Colors.RED, visible=False)

    def validacao_login(e):
        for conta in read():
            if nome_login.value in conta and senha_login.value in conta:
                mensagem_erro.visible = False
                ir_para_tela_principal()
                return
        senha_login.value = ""
        mensagem_erro.visible = True
        nome_login.focus()
        page.update()

    def ir_para_tela_cadastro(e):
        page.views.append(tela_cadastro())
        page.update()

    def back_to_login(e=None):
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
                            ft.TextButton("Ainda não tem uma conta? Cadastre-se", on_click=ir_para_tela_cadastro),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            ]
        )

    # Cadastro ---------------------------------------
    nome_cadastro = ft.TextField(label="Nome de usuário", width=300)
    email_cadastro = ft.TextField(label="E-mail", width=300)
    senha_cadastro = ft.TextField(label="Senha (mínimo 6 dígitos)", password=True, can_reveal_password=True, width=300)
    confirmar_senha = ft.TextField(label="Confirmar senha", password=True, can_reveal_password=True, width=300)
    erro_nome = ft.Text("", color=ft.Colors.RED, visible=False)
    erro_email = ft.Text("", color=ft.Colors.RED, visible=False)
    erro_senha = ft.Text("", color=ft.Colors.RED, visible=False)
    erro_confirmar_senha = ft.Text("", color=ft.Colors.RED, visible=False)

    def validar_cadastro(e):
        erro_nome.visible = erro_email.visible = erro_senha.visible = erro_confirmar_senha.visible = False
        erro_nome.value = erro_email.value = erro_senha.value = erro_confirmar_senha.value = ""
        page.update()

        nome = nome_cadastro.value.strip()
        email = email_cadastro.value.strip()
        senha = senha_cadastro.value.strip()

        for conta in read():
            if nome in conta:
                erro_nome.value = "Usuário já existe!"
                erro_nome.visible = True
                page.update()
                return
            if email in conta:
                erro_email.value = "Esse e-mail está vinculado a uma conta!"
                erro_email.visible = True
                page.update()
                return

        if ' ' in nome:
            erro_nome.value = "Não é permitido espaços em branco!"
            erro_nome.visible = True
            page.update()
            return

        if not (2 <= len(nome) <= 8):
            erro_nome.value = "Permitido apenas entre 2 e 8 caracteres!"
            erro_nome.visible = True
            page.update()
            return

        if not ("@gmail.com" in email) or ' ' in email or email == '':
            erro_email.value = "E-mail inválido!"
            erro_email.visible = True
            page.update()
            return

        if not (6 <= len(senha)):
            erro_senha.value = "Deve conter 6 ou mais dígitos!"
            erro_senha.visible = True
            page.update()
            return

        if confirmar_senha.value.strip() != senha:
            erro_confirmar_senha.value = "As duas senhas devem ser iguais!"
            erro_confirmar_senha.visible = True
            page.update()
            return

        create(nome, email, senha)
        page.update()
        back_to_login()

    def tela_cadastro():
        nome_cadastro.value = email_cadastro.value = senha_cadastro.value = confirmar_senha.value = ""
        erro_nome.visible = erro_email.visible = erro_senha.visible = erro_confirmar_senha.visible = False
        page.update()
        return ft.View(
            "/register",
            controls=[
                ft.Text("Cadastre-se", size=30, weight="bold"),
                nome_cadastro,
                erro_nome,
                email_cadastro,
                erro_email,
                senha_cadastro,
                erro_senha,
                confirmar_senha,
                erro_confirmar_senha,
                ft.ElevatedButton("Criar conta", on_click=validar_cadastro),
                ft.TextButton("Já tem uma conta? Faça login", on_click=back_to_login)
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Tela principal -----------------------------------
    def adicionar_novo_idioma(e):
        mostrar_input_idioma.current.visible = True
        input_novo_idioma.current.focus()
        page.update()

    def confirmar_idioma(e):
        novo = input_novo_idioma.current.value.strip()
        if novo:
            menu_idiomas.current.controls.insert(-2, ft.TextButton(novo, style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=selecionar_idioma, data=novo))
            input_novo_idioma.current.value = ""
            mostrar_input_idioma.current.visible = False
            page.update()

    def selecionar_idioma(e):
        idioma_atual.current.value = f"Minhas palavras em {e.control.data}"
        page.update()

    def adicionar_palavra(e=None):
        texto = nova_palavra.current.value.strip()
        if texto:
            lista_palavras.current.controls.append(ft.Text(f"• {texto}"))
            nova_palavra.current.value = ""
            page.update()

    # Função para mostrar o campo de texto para novo idioma
    def mostrar_input_idioma(e):
        mostrar_input.current.visible = True
        campo_idioma.current.focus()
        page.update()
    
    # Função para adicionar um novo idioma
    def adicionar_idioma(e):
        nome = campo_idioma.current.value.strip().capitalize()
        if nome:
            lista_idiomas.current.controls.append(
                ft.TextButton(nome, style=ft.ButtonStyle(color=ft.Colors.WHITE), data=nome, on_click=selecionar_idioma)
            )
            campo_idioma.current.value = ""
            mostrar_input.current.visible = False
            page.update()

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
                # Topo fixo
                ft.Row([
                    ft.Text("Idiomas", size=22, weight="bold", color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                ]),
                
                # Área com scroll apenas nos idiomas
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=5,
                        controls=[
                            ft.Column(
                                ref=lista_idiomas,
                                controls=[
                                    ft.TextButton("Inglês", style=ft.ButtonStyle(color=ft.Colors.WHITE), data="Inglês", on_click=selecionar_idioma),
                                ]
                            ),
                            ft.Divider(color=ft.Colors.WHITE),
                            ft.TextButton("+ Adicionar novo idioma", style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=mostrar_input_idioma),
                            ft.Container(
                                ref=mostrar_input,
                                visible=False,
                                content=ft.Row([
                                    ft.TextField(ref=campo_idioma, hint_text="Nome do idioma", width=120, dense=True, height=40),
                                    ft.IconButton(icon=ft.Icons.CHECK, icon_color=ft.Colors.GREEN, on_click=adicionar_idioma),
                                ])
                            )
                        ]
                    )
                )
            ]
        )
    )


    nova_palavra = ft.Ref[ft.TextField]()
    lista_palavras = ft.Ref[ft.Column]()

    conteudo = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            expand=True,
            spacing=25,
            controls=[
                ft.Row([
                    ft.Text(ref=idioma_atual, value="Minhas palavras em Inglês", size=24, weight="bold"),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.BLUE_GREY),
                    ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.BLUE_GREY, on_click=back_to_login)
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
                                ft.Column(ref=lista_palavras, spacing=5)
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
                                ft.TextField(ref=nova_palavra, label="Nova palavra"),
                                ft.ElevatedButton("Adicionar", color=ft.Colors.GREY_100, icon=ft.Icons.ADD, on_click=adicionar_palavra)
                            ])
                        )
                    ]
                )
            ]
        )
    )

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
                            controls=[menu_lateral, conteudo]
                        )
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            )
        )
        page.go("/principal")

    page.views.append(login())
    page.update()

ft.app(target=main)
