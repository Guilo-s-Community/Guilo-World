
import os
import tkinter
from PIL import ImageTk, Image
import customtkinter
import calculos
from matplotlib import pyplot as plt

plt.style.use('ggplot')

calculos.larguraPocoE

#fazer todos os calculos (X)
    #proton (X)    #eletron (X)
#separar direito (X)
#printar as respostas na label (X)
#gráfico (X)
#simulação ( )



customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



#FORMATANDO AS RESPOSTAS PARA NOTAÇÃO CIENTÍFICA
def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]


def set_text(label, txt):
    text = label.cget("text").splitlines()[0]
    label.configure(text=f"{text}\n{txt}")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Projeto de Física")

        self.iconbitmap('feliz.ico')
        self.geometry(f"{1150}x{690}")
        self.minsize(1150,690)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)



        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Opções", font=customtkinter.CTkFont(size=20, weight="bold"),text_color="#296cc4")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text='Simulação do Poço', command=self.sidebar_button_event1)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text='Gráfico Onda', command=self.sidebar_button_event2)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text='Gráfico Probabilidade', command=self.sidebar_button_event3)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Modo de Aparência", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=300)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Primeira Função Elétron")
        self.tabview.add("Primeira Função Próton")
        self.tabview.add("Segunda Função Elétron/Próton")


        #LABEL DOS BOTÕES DA SEGUNDA FUNÇÃO EM ELÉTRON
        self.string_input_button_1_1 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text="A - 𝜓x=A*sin(K∙X)",
                                                           command=self.open_input_dialog_event_A)
        self.string_input_button_1_2 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text="K - 𝜓x=A*sin(K∙X)",
                                                           command=self.open_input_dialog_event_K)
        self.string_input_button_1_3 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text="X - 𝜓x=A*sin(K∙X)",
                                                           command=self.open_input_dialog_event_X)
        #SEGUNDA FUNÇÃO ELETRON LABEL DAS RESPOSTAS
        self.label_resposta_largura_e = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Largura do poço (m) - Elétron",text_color="#296cc4")
        self.label_resposta_largura_e.grid(row=0, column=1, padx=20, pady=(10, 10))
        self.label_resposta_N_e = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Valor de N - Elétron",text_color="#296cc4")
        self.label_resposta_N_e.grid(row=1, column=1, padx=20, pady=(10, 10))
        self.label_resposta_Probabilidade_e = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Probabilidade (%) - Elétron",text_color="#296cc4")
        self.label_resposta_Probabilidade_e.grid(row=2, column=1, padx=20, pady=(10, 10))

        self.label_resposta_largura = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="-----------------------------------------------------------------------",text_color="#296cc4")
        self.label_resposta_largura.grid(row=0, column=2, padx=20, pady=(10, 10))
        self.label_resposta_N = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="-----------------------------------------------------------------------",text_color="#296cc4")
        self.label_resposta_N.grid(row=1, column=2, padx=20, pady=(10, 10))
        self.label_resposta_Probabilidade = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="-----------------------------------------------------------------------",text_color="#296cc4")
        self.label_resposta_Probabilidade.grid(row=2, column=2, padx=20, pady=(10, 10))

        self.label_resposta_largura_p = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Largura do poço (m) - Próton ",text_color="#296cc4")
        self.label_resposta_largura_p.grid(row=0, column=3, padx=20, pady=(10, 10))
        self.label_resposta_N_p = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Valor de N - Próton",text_color="#296cc4")
        self.label_resposta_N_p.grid(row=1, column=3, padx=20, pady=(10, 10))
        self.label_resposta_Probabilidade_p = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"), text="Probabilidade (%) - Próton",text_color="#296cc4")
        self.label_resposta_Probabilidade_p.grid(row=2, column=3, padx=20, pady=(10, 10))

        self.string_input_button_1_1.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.string_input_button_1_2.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button_1_3.grid(row=2, column=0, padx=20, pady=(10, 10))


        self.string_input_button_inv1 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text=" ")
        self.string_input_button_inv1.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.string_input_button_inv2 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text=" ")
        self.string_input_button_inv2.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.calculo1 = customtkinter.CTkButton(self.tabview.tab("Segunda Função Elétron/Próton"), text="Calcular",command=self.calcular3_onclick
                                                           )
        self.calculo1.grid(row=5, column=0, padx=20, pady=(10, 10))




        # imgaemOriginal1 = Image.open("gatoteste.png")
        # iamgemAjustada1 = imgaemOriginal1.resize((200,125))
        # imagemDefinida1 = ImageTk.PhotoImage(iamgemAjustada1)

        # imgaemOriginal2 = Image.open("gatoteste2.webp")
        # iamgemAjustada2 = imgaemOriginal2.resize((400,125))
        # imagemDefinida2 = ImageTk.PhotoImage(iamgemAjustada2)

        # self.label_imagem = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"),text='',image=imagemDefinida1)
        # self.label_imagem.grid(row=6,column=0, padx=0, pady=(20,0))
        # self.label_imagem = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"),text='',image=imagemDefinida1)
        # self.label_imagem.grid(row=6,column=0, padx=0, pady=(20,0))
        # self.label_imagem = customtkinter.CTkLabel(self.tabview.tab("Segunda Função Elétron/Próton"),text='',image=imagemDefinida1)
        # self.label_imagem.grid(row=6,column=0, padx=0, pady=(20,0))



        #LABEL DOS BOTÕES DA PRIMEIRA FUNÇÃO ELÉTRON
        self.string_input_button_2_1 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Largura do Poço",command=self.open_input_dialog_event_largura)
        self.string_input_button_2_1.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_2 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Valor de N Inicial",command=self.open_input_dialog_event_ninicial)
        self.string_input_button_2_2.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_3 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Valor de N Final",command=self.open_input_dialog_event_nfinal)
        self.string_input_button_2_3.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_4 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Integral A",command=self.open_input_dialog_event_integralA)
        self.string_input_button_2_4.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_5 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Integral B",command=self.open_input_dialog_event_integralB)
        self.string_input_button_2_5.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.calcular1 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Elétron"), text="Calcular", command=self.calcular1_onclick)
        self.calcular1.grid(row=5, column=0, padx=20, pady=(10, 10))



        #PRIMEIRA FUNÇÃO (ELÉTRON) LABEL DOS PRINTS



        #LABEL DOS BOTÕES DA PRIMEIRA FUNÇÃO PRÓTON
        self.string_input_button_2_1 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Largura do Poço",command=self.open_input_dialog_event_largura)
        self.string_input_button_2_1.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_2 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Valor de N Inicial",command=self.open_input_dialog_event_ninicial)
        self.string_input_button_2_2.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_3 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Valor de N Final",command=self.open_input_dialog_event_nfinal)
        self.string_input_button_2_3.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_4 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Integral A",command=self.open_input_dialog_event_integralA)
        self.string_input_button_2_4.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.string_input_button_2_5 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Integral B",command=self.open_input_dialog_event_integralB)
        self.string_input_button_2_5.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.calcular2 = customtkinter.CTkButton(self.tabview.tab("Primeira Função Próton"), text="Calcular",command=self.calcular2_onclick)
        self.calcular2.grid(row=5, column=0, padx=20, pady=(10, 10))




        #PRIMEIRA FUNÇÃO ELÉTRON LABEL DAS RESPOSTAS
        self.label_respostas_a_ele = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"),text='Valor de A (1/√m)',text_color="#296cc4")
        self.label_respostas_a_ele.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.label_respostas_frequencia  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"),text='Valor da Frequência (Hz)',text_color="#296cc4")
        self.label_respostas_frequencia.grid(row=1, column=1, padx=20, pady=(10, 10))

        self.label_respostas_kxinicial_ele  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Valor de Kx Inicial (1/m)",text_color="#296cc4")
        self.label_respostas_kxinicial_ele.grid(row=2, column=1, padx=20, pady=(10, 10))

        self.label_respostas_kxfinal_ele  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Valor de Kx Final (1/m)",text_color="#296cc4")
        self.label_respostas_kxfinal_ele.grid(row=3, column=1, padx=20, pady=(10, 10))

        self.label_respostas_energiainicialEvEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Energia Inicial (eV)",text_color="#296cc4")
        self.label_respostas_energiainicialEvEle.grid(row=0, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiafinalEvEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Energia Final (eV)",text_color="#296cc4")
        self.label_respostas_energiafinalEvEle.grid(row=1, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiainicialJEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Energia Inicial (J)",text_color="#296cc4")
        self.label_respostas_energiainicialJEle.grid(row=2, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiafinalJEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Energia Final (J)",text_color="#296cc4")
        self.label_respostas_energiafinalJEle.grid(row=3, column=2, padx=20, pady=(10, 10))

        self.label_respostas_eabsorvidoEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Energia Absorvida (eV)",text_color="#296cc4")
        self.label_respostas_eabsorvidoEle.grid(row=0, column=3, padx=20, pady=(10, 10))

        self.label_respostas_CompOnda_ele  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Comprimento de Onda (m)",text_color="#296cc4")
        self.label_respostas_CompOnda_ele .grid(row=1, column=3, padx=20, pady=(10, 10))

        self.label_respostas_vinicialELe = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Velocidade Inicial (m/s)",text_color="#296cc4")
        self.label_respostas_vinicialELe.grid(row=2, column=3, padx=20, pady=(10, 10))

        self.label_respostas_vfinalEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Velocidade Final (m/s)",text_color="#296cc4")
        self.label_respostas_vfinalEle.grid(row=3, column=3, padx=20, pady=(10, 10))

        self.label_respostas_lambidaInicialEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Lambda do nível inicial (m)",text_color="#296cc4")
        self.label_respostas_lambidaInicialEle.grid(row=0, column=4, padx=20, pady=(10, 10))

        self.label_respostas_lambidaFinalEle = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Lambda do nível final (m)",text_color="#296cc4")
        self.label_respostas_lambidaFinalEle.grid(row=1, column=4, padx=20, pady=(10, 10))

        self.label_respostas_integralI_ele  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Probabilidade nível inicial (%)",text_color="#296cc4")
        self.label_respostas_integralI_ele .grid(row=2, column=4, padx=20, pady=(10, 10))

        self.label_respostas_integralF_ele  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Elétron"), text="Probabilidade nível final (%)",text_color="#296cc4")
        self.label_respostas_integralF_ele .grid(row=3, column=4, padx=20, pady=(10, 10))




        #create main entry and button
        #self.entry = customtkinter.CTkEntry(self, placeholder_text="Teste")
        #self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")


        #self.main_button_1 = customtkinter.CTkButton(master=self,text="Teste", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        #self.textbox = customtkinter.CTkTextbox(self, width=250)
        #self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")




        #-----------------------------------------FIM ELÉTRON -------------------------------------------------------------------


        #PRIMEIRA FUNÇÃO PRÓTON LABEL DAS RESPOSTAS
        self.label_respostas_a_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Valor de A (1/√m)",text_color="#296cc4")
        self.label_respostas_a_proton.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.label_respostas_frequencia_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Valor da Frequência(Hz)",text_color="#296cc4")
        self.label_respostas_frequencia_proton.grid(row=1, column=1, padx=20, pady=(10, 10))

        self.label_respostas_kxinicial_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Valor de Kx Inicial (1/m)",text_color="#296cc4")
        self.label_respostas_kxinicial_proton.grid(row=2, column=1, padx=20, pady=(10, 10))

        self.label_respostas_kxfinal_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Valor de Kx Final (1/m)",text_color="#296cc4")
        self.label_respostas_kxfinal_proton.grid(row=3, column=1, padx=20, pady=(10, 10))

        self.label_respostas_energiainicialEv_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Energia Inicial (eV)",text_color="#296cc4")
        self.label_respostas_energiainicialEv_proton.grid(row=0, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiafinalEv_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Energia Final (eV)",text_color="#296cc4")
        self.label_respostas_energiafinalEv_proton.grid(row=1, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiainicialJ_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Energia Inicial (J)",text_color="#296cc4")
        self.label_respostas_energiainicialJ_proton.grid(row=2, column=2, padx=20, pady=(10, 10))

        self.label_respostas_energiafinalJ_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Energia Final (J)",text_color="#296cc4")
        self.label_respostas_energiafinalJ_proton.grid(row=3, column=2, padx=20, pady=(10, 10))

        self.label_respostas_eabsorvido_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Energia Absorvida (eV)",text_color="#296cc4")
        self.label_respostas_eabsorvido_proton.grid(row=0, column=3, padx=20, pady=(10, 10))

        self.label_respostas_CompOnda_proton  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Comprimento de Onda (m)",text_color="#296cc4")
        self.label_respostas_CompOnda_proton .grid(row=1, column=3, padx=20, pady=(10, 10))

        self.label_respostas_vinicial_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Velocidade Inicial (m/s)",text_color="#296cc4")
        self.label_respostas_vinicial_proton.grid(row=2, column=3, padx=20, pady=(10, 10))

        self.label_respostas_vfinal_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Velocidade Final (m/s)",text_color="#296cc4")
        self.label_respostas_vfinal_proton.grid(row=3, column=3, padx=20, pady=(10, 10))

        self.label_respostas_lambidaInicial_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Lambda do nível inicial (m)",text_color="#296cc4")
        self.label_respostas_lambidaInicial_proton.grid(row=0, column=4, padx=20, pady=(10, 10))

        self.label_respostas_lambidaFinal_proton = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Lambda do nível final (m)",text_color="#296cc4")
        self.label_respostas_lambidaFinal_proton.grid(row=1, column=4, padx=20, pady=(10, 10))

        self.label_respostas_integralI_proton  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Probabilidade nível inicial (%)",text_color="#296cc4")
        self.label_respostas_integralI_proton .grid(row=2, column=4, padx=20, pady=(10, 10))

        self.label_respostas_integralF_proton  = customtkinter.CTkLabel(self.tabview.tab("Primeira Função Próton"), text="Probabilidade nível final (%)",text_color="#296cc4")
        self.label_respostas_integralF_proton .grid(row=3, column=4, padx=20, pady=(10, 10))
        #---------------------------------FIM PROTON------------------------------------------------------------------------


        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.textbox = customtkinter.CTkTextbox(self,text_color="#296cc4",width = 250)
        self.textbox.grid(row=1, column=1,padx=(20,20), pady=(10, 0),sticky='nsew')

        self.textbox.insert("0.0","Poço de Potencial Infinito\n\n"+
                            "Princípio de Confinamento\nO confinamento de ondas de qualquer tipo (ondas em uma corda, ondas do mar, ondas luminosas e ondas de matéria) leva à quantização, ou seja, à existência\nde estados discretos com energias discretas. Estados intermediários com valores intermediários de energia não são possíveis."+
                            "\n\nDualidade onda-partícula\nA dualidade onda-partícula passou a ser questionada quando os resultados experimentais de Heinrich Hertz referentes ao efeito fotoelétrico entraram\nem contradição direta com aquilo que era esperado para o comportamento da luz, de acordo com a teoria eletromagnética de James Clerk Maxwell.\nSegundo a teoria vigente da época, qualquer frequência de luz deveria ser capaz de ejetar elétrons de uma folha metálica, entretanto, os resultados de Hertz\nmostraram que era somente a partir de certas frequências que se detectava tal emissão."+
                            "\n\nEm 1923, Louis De Broglie sugeriu que as partículas também fossem capazes de se comportar como ondas. A hipótese de De Broglie, como ficou conhecida,\nsugeriu a existência de “ondas de partículas”, com isso, era esperado que elétrons, prótons e outras partículas subatômicas pudessem apresentar efeitos\naté então exclusivamente ondulatórios, como refração (mudança de velocidade das ondas), difração (capacidade das ondas de contornar obstáculos) etc.\nA hipóteste de De Broglie foi confirmada, em 1928, pelo experimento de Davisson-Germer, que consistia em promover a difração de elétrons.\nPara que isso fosse feito, um feixe catódico era direcionado a um alvo de níquel que podia ser rotacionado, de modo a alterar o ângulo em que o\nfeixe de elétrons incidia sobre o plano de átomos de níquel."+
                            "\n\nA explicação para a dualidade onda-partícula surgiu com o avanço da mecânica quântica. Atualmente, sabe-se que todos os sistemas quânticos são regidos por um mecanismo conhecido como princípio da incerteza de Heisenberg. Segundo esse princípio, as partículas são como um “campo de matéria”, uma vez que\nnão é possível determinar com absoluta certeza a posição de uma partícula quântica.A partir do desenvolvimento da equação de Schroedinger, passamos\na entender que todas as partículas são completamente caracterizadas por uma função de onda, que nada mais é do que uma expressão matemática\nque carrega consigo toda a informação que pode ser extraída daquela partícula. Antes de observarmos um sistema quântico, suas informações\nsão indeterminadas, depois de observadas, é possível localizá-las e medi-las, nesse caso, dizemos que sua função de onda sofreu um colapso,\napresentando-se em um de seus possíveis estados. Em outras palavras, o que determina se uma entidade quântica é uma onda ou uma partícula é o próprio ato da observação, pois é possível que se realize um experimento e se observe um comportamento corpuscular e um outro experimento revele um comportamento\nondulatório.\nTudo graças às probabilidades da física quântica."+
                            "\n\n\nO poço de potencial representa a energia potencial em forma de poço envolvida num certo sistema e pode ser qualificado como finito ou infinito.\nUm poço de potencial é a região em torno de um mínimo local de energia potencial que, por sua vez, é a forma de energia que está associada a um certo\nsistema, no qual ocorre interações entre diferentes corpos, e está relacionada com a posição que determinado corpo ocupa.\nA energia potencial de um sistema pode ter quatro origens distintas que estão correlacionadas as quatro forças fundamentais da natureza:\nforça eletromagnética, força gravitacional, força fraca e força forte.\nSob uma perspectiva quântica, o poço de potencial representa o confinamento quântico da partícula em questão e pode provocar a quantização da energia da mesma, o que, classicamente, não acontece.")

    def open_input_dialog_event_largura(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="Digite o valor da largura (m)", title="Largura")
        self.largura = float(dialog.get_input())

    def open_input_dialog_event_ninicial(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="Digite o valor do Nivel Inicial", title="Nivel Inicial")
        self.ninicial = float(dialog.get_input())

    def open_input_dialog_event_nfinal(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="Digite o valor do Nivel Final", title="Nivel Final")
        self.nfinal = float(dialog.get_input())

    def open_input_dialog_event_integralA(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="Digite o valor da Integral A", title="Integral A")
        self.integralA = float(dialog.get_input())

    def open_input_dialog_event_integralB(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="Digite o valor da Integral B", title="Integral B")

        self.integralB = float(dialog.get_input())

    def open_input_dialog_event_A(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="𝜓(x) = A *sin(K ∙ X)\nDigite o valor de A", title="𝜓(x) = A *sin(K ∙ X)")
        self.A = float(dialog.get_input())

    def open_input_dialog_event_K(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="𝜓(x) = A *sin(K ∙ X)\nDigite o valor de K", title="𝜓(x) = A *sin(K ∙ X)")
        self.K = float(dialog.get_input())

    def open_input_dialog_event_X(self):
        dialog = customtkinter.CTkInputDialog(entry_border_color='#296cc4',text="𝜓(x) = A *sin(K ∙ X)\nDigite o valor de X", title="𝜓(x) = A *sin(K ∙ X)")
        self.X = float(dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def calcular1_onclick(self):
        _, k1 = calculos.funcaoQuanticaInicial(self.ninicial,self.largura)
        Eij, Eiv, Efj, Efv = calculos.energiaQuanticaEletron(self.ninicial, self.nfinal, self.largura)
        A, k2 = calculos.funcaoQuanticaFinal(self.nfinal, self.largura)
        eabsorvido, CompOnda, f = calculos.calculoFoton(Eiv,Efv)
        vinicial, vfinal = calculos.velocidadeEletron(Eij,Efj)
        lambiaInicialEle , lambidaFinalEle = calculos.comprimentoDeBroglieEletron(vinicial, vfinal)
        integralI = calculos.probabilidadeIntegralNi(A, k1, self.integralA, self.integralB)
        integralF = calculos.probabilidadeIntegralNf(A, k2, self.integralA, self.integralB)
        set_text(self.label_respostas_a_ele, format_e(A))
        set_text(self.label_respostas_frequencia, format_e(f))
        set_text(self.label_respostas_kxinicial_ele, format_e(k1))
        set_text(self.label_respostas_kxfinal_ele, format_e(k2))
        set_text(self.label_respostas_energiainicialEvEle, format_e(Eiv))
        set_text(self.label_respostas_energiainicialJEle, format_e(Eij))
        set_text(self.label_respostas_energiafinalEvEle, format_e(Efv))
        set_text(self.label_respostas_energiafinalJEle, format_e(Efj))
        set_text(self.label_respostas_eabsorvidoEle, format_e(eabsorvido))
        set_text(self.label_respostas_CompOnda_ele, format_e( CompOnda))
        set_text(self.label_respostas_vinicialELe, format_e(vinicial))
        set_text(self.label_respostas_vfinalEle, format_e( vfinal))
        set_text(self.label_respostas_lambidaInicialEle, format_e(lambiaInicialEle))
        set_text(self.label_respostas_lambidaFinalEle, format_e(lambidaFinalEle))
        set_text(self.label_respostas_integralI_ele, format_e(integralI))
        set_text(self.label_respostas_integralF_ele, format_e( integralF))
        ...

    def calcular2_onclick(self):
        _, k1 = calculos.funcaoQuanticaInicial(self.ninicial,self.largura)
        Eij, Eiv, Efj, Efv = calculos.energiaQuanticaProton(self.ninicial, self.nfinal, self.largura)
        A, k2 = calculos.funcaoQuanticaFinal(self.nfinal, self.largura)
        eabsorvido, CompOnda, f = calculos.calculoFoton(Eiv,Efv)
        vinicial, vfinal = calculos.velocidadeProton(Eij,Efj)
        lambiaInicialPro , lambidaFinalPro = calculos.comprimentoDeBroglieProton(vinicial, vfinal)
        integralI = calculos.probabilidadeIntegralNi(A, k1, self.integralA, self.integralB)
        integralF = calculos.probabilidadeIntegralNf(A, k2, self.integralA, self.integralB)
        set_text(self.label_respostas_a_proton, format_e(A))
        set_text(self.label_respostas_frequencia_proton, format_e(f))
        set_text(self.label_respostas_kxinicial_proton, format_e(k1))
        set_text(self.label_respostas_kxfinal_proton, format_e(k2))
        set_text(self.label_respostas_energiainicialEv_proton, format_e(Eiv))
        set_text(self.label_respostas_energiainicialJ_proton, format_e(Eij))
        set_text(self.label_respostas_energiafinalEv_proton, format_e(Efv))
        set_text(self.label_respostas_energiafinalJ_proton, format_e(Efj))
        set_text(self.label_respostas_eabsorvido_proton, format_e(eabsorvido))
        set_text(self.label_respostas_CompOnda_proton, format_e( CompOnda))
        set_text(self.label_respostas_vinicial_proton, format_e(vinicial))
        set_text(self.label_respostas_vfinal_proton, format_e( vfinal))
        set_text(self.label_respostas_lambidaInicial_proton, format_e(lambiaInicialPro))
        set_text(self.label_respostas_lambidaFinal_proton, format_e(lambidaFinalPro))
        set_text(self.label_respostas_integralI_proton, format_e(integralI))
        set_text(self.label_respostas_integralF_proton, format_e( integralF))
        ...




    def calcular3_onclick(self):
        larguraE = calculos.larguraPocoE(self.A)
        nE = calculos.numeroQuanticoE(larguraE, self.K)
        probabilidadeE = calculos.numeroQuanticoE(larguraE,nE)
        set_text(self.label_resposta_largura_e, format_e(larguraE))
        set_text(self.label_resposta_N_e, format_e(nE))
        set_text(self.label_resposta_Probabilidade_e, format_e(probabilidadeE))

        larguraP = calculos.larguraPocoP(self.A)
        nP = calculos.numeroQuanticoP(larguraP, self.X)
        probabilidadeP = calculos.numeroQuanticoP(larguraP,nP)
        set_text(self.label_resposta_largura_p, format_e(larguraP))
        set_text(self.label_resposta_N_p, format_e(nP))
        set_text(self.label_resposta_Probabilidade_p, format_e(probabilidadeP))


    def sidebar_button_event1(self):
        os.system('simulacao.mp4')
    def sidebar_button_event2(self):
        _, k1 = calculos.funcaoQuanticaInicial(self.ninicial,self.largura)
        A, k2 = calculos.funcaoQuanticaFinal(self.nfinal, self.largura)
        calculos.GraficosOndas(A, k1, k2, self.ninicial, self.nfinal, self.largura)
        plt.show()

    def sidebar_button_event3(self):
        _, k1 = calculos.funcaoQuanticaInicial(self.ninicial,self.largura)
        A, k2 = calculos.funcaoQuanticaFinal(self.nfinal, self.largura)
        calculos.GraficosProbabilidade(A, k1, k2, self.ninicial, self.nfinal, self.largura)
        plt.show()





if __name__ == "__main__":
    app = App()
    app.mainloop()

