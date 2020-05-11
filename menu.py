def interfacemenu():

    import PySimpleGUI as sg
    import MySQLdb
    from funcoes import menu


    table=[]
    sg.theme("Reddit")
    fundo="bd.png"
    fundo=sg.Image(fundo)
    #layout = [[sg.Button(image_filename="bd.png",image_subsample=4,enable_events=False)]
    layout = [[sg.Text("\n\n"),sg.Button('Inserir',image_filename="inserir.png",image_subsample=10),
               sg.Button('Listar',image_filename="listar.png",image_subsample=10),
               sg.Button('Atualizar',image_filename="atualizar.png",image_subsample=10),sg.Button('Deletar',image_filename="deletar.png",image_subsample=10),
               sg.Button('Venda',image_filename="venda.png",image_subsample=10)],
              [sg.Text("  Inserir               Listar              Atualizar             Deletar                Venda")],
            ]

    window=sg.Window("Shop",layout,size=(650,200),alpha_channel=0.8,grab_anywhere=True,
                     no_titlebar=False,button_color=("black","black"),
                     font=(("Arial Black"),11),ttk_theme="vista",auto_size_buttons=False,use_ttk_buttons=True,	keep_on_top=True
                     ,resizable=True,icon="icone.ico")

    while True:

        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        op = str(event)
        if op=='Sair':
            break
        menu(op)

