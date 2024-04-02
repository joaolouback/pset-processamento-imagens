# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: João Pedro Estevão Louback
#    Matrícula: 202305625
#    Turma: CC3M-A
#    Email: jpestevaoloubackbr@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


def caixa_desfoque(n):
    # Cria um kernel de desfoque de caixa de tamanho n x n.
    valor = 1 / (n * n)
    return [[valor] * n for _ in range(n)]

# Classe Imagem:


class Imagem:
    # Inicializa uma instância da classe Imagem com a largura, altura e pixels fornecidos
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # Obtém o valor do pixel nas coordenadas (x, y) da imagem.
        # Se as coordenadas estiverem fora dos limites da imagem, os valores são ajustados para os limites mais próximos
        if x < 0:
            x = 0
        elif x >= self.largura:
            x = self.largura - 1      # <--
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1       # <--

        return self.pixels[(x + y * self.largura)]

    def set_pixel(self, x, y, c):
        # Define o valor do pixel nas coordenadas (x, y) da imagem para o valor fornecido
        self.pixels[(x + y * self.largura)] = c

    def aplicar_por_pixel(self, func):
        # Aplica uma função a cada pixel da imagem e retorna uma nova instância de Imagem com os pixels transformados
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    # Correlação kernel
    def correlacao(self, kn):
        # Realiza a correlação entre a imagem e um kernel dado e retorna a imagem resultante
        k = len(kn)
        centro = k // 2
        final_img = Imagem.nova(self.largura, self.altura)

        for x in range(final_img.largura):
            for y in range(final_img.altura):
                novacor = 0
                for w in range(k):
                    for h in range(k):
                        x1 = x - centro + h
                        y1 = y - centro + w
                        novacor += self.get_pixel(x1, y1) * kn[w][h]

                final_img.set_pixel(x, y, novacor)

        return final_img

    def invertida(self):
        # Implementação da inversão dos pixels
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrada(self, n):
        # Aplica um efeito de desfoque à imagem com um kernel de desfoque de caixa de tamanho n x n.
        kernel = caixa_desfoque(n)
        return self.correlacao(kernel)

    def focada(self, n):
        # Criar o kernel de desfoque de caixa
        kernel_desfoque = caixa_desfoque(n)

        # Aplicar a correlação com o kernel de desfoque de caixa
        imagem_desfocada = self.correlacao(kernel_desfoque)

        # Criar a imagem nítida (máscara de não nitidez)
        imagem_nitida = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                valor_nitido = 2 * \
                    self.get_pixel(x, y) - imagem_desfocada.get_pixel(x, y)
                # Garantir que o pixel resultante esteja no intervalo [0, 255]
                valor_nitido = max(0, min(valor_nitido, 255))
                imagem_nitida.set_pixel(x, y, valor_nitido)

        return imagem_nitida

    def bordas(self):
        # Detecta bordas na imagem usando o operador Sobel.
        # Aplica o kernel Kx
        kernel_Kx = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        imagem_Ox = self.correlacao(kernel_Kx)

        # Aplicar o kernel Ky
        kernel_Ky = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
        imagem_Oy = self.correlacao(kernel_Ky)

        # Calcular a imagem final com a raiz quadrada da soma dos quadrados de Ox e Oy
        imagem_final = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                valor_Ox = imagem_Ox.get_pixel(x, y)
                valor_Oy = imagem_Oy.get_pixel(x, y)
                valor_final = round(math.sqrt(valor_Ox ** 2 + valor_Oy ** 2))
        # Garante que o pixel resultante esteja no intervalo [0, 255]
                valor_final = max(0, min(valor_final, 255))
                imagem_final.set_pixel(x, y, valor_final)

        return imagem_final

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """

        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                          for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(
                mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize(
                (event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(
                data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(
            height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def refaz_apos():
        tcl.after(500, refaz_apos)

    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.

    pass

    # QUESTÃO 1 - Teste com o filtro de inversão da Imagem(4, 1, [29, 89, 136, 200])
    # imagem 4 x 1

    # imagem_teste = Imagem(4, 1, [29, 89, 136, 200])
    # imagem_invertida = imagem_teste.invertida()
    # print("Pixels da imagem invertida:", imagem_invertida.pixels)

    # Comparação dos valores dos pixels com os valores esperados
    # esperado = Imagem(4, 1, [226, 166, 119, 55])
    # if imagem_invertida.pixels == esperado.pixels:
    #    print("Os pixels da imagem invertida correspondem aos pixels esperados.")
    # else:
    #    print("Os pixels da imagem invertida NÃO correspondem aos pixels esperados.")

    # Resposta:
    # O output esperado dos pixels seria [226, 166, 119, 55].
    # Para obtê-lo, basta subtrair os valores de cada um dos pixels originais ([29, 89, 136, 200]) de 255.
    # Calculo:
    # 255 - 29 = 226
    # 255 - 89 = 166
    # 255 - 136 = 119
    # 255 - 55 = 200

    # QUESTÃO 2 - Teste com o filtro de inversão da Imagem do Peixe. Deve salvar e mostrar a imagem invertida
    # Exemplo de uso do filtro de inversão na imagem bluegill.png

    # imagem_Peixe = Imagem.carregar('test_images/bluegill.png')
    # imagem_PeixeInvertida = imagem_Peixe.invertida()

    # Salvar a imagem invertida como um arquivo PNG
    # imagem_PeixeInvertida.salvar('bluegill_invertida.png')

    # Mostrar a imagem invertida
    # imagem_PeixeInvertida.mostrar()

    # QUESTÃO 3 - Teste da imagem com kernel
    # Crie uma instância da classe Imagem com os valores da imagem de entrada

    # imagem_entrada = Imagem(3, 3, [80, 53, 99, 129, 127, 148, 175, 174, 193])

    # Defina o kernel
    # kernel = [
    #    [0.00, -0.07, 0.00],
    #    [-0.45, 1.20, -0.25],
    #    [0.00, -0.12, 0.00]
    # ]

    # Chame a função correlacao passando o kernel como argumento
    # imagem_resultante = imagem_entrada.correlacao(kernel)

    # valor_pixel = imagem_resultante.get_pixel(1, 1)

    # print("Valor do pixel na posição (1, 1):", valor_pixel)

    # Resposta:
    # Usando a formula disposta pelo professor é realizado o calculo, portanto o resultado é aproximadamente 32.76
    # 0.00 x 80 = 0
    # -0,07 x 53 = -3, 71
    # 0.00 x 99 = 0
    # -0.45 x 129 = -58.05
    # 1.20 x 127 = 152.4
    # -0.25 x 148 = -37
    # 0.00 x 175 = 0
    # -0.12 x 174 = -20.88
    # 0.00 x 193 = 0
    # Pixel = 0 + (-3, 71) + 0 + (-58.05) + 152.4 + -37 + 0 + -20.88 + 0 = 32.76.

    # Questão 4- Imagem do Porco

    # imagem_Porco = Imagem.carregar('test_images/pigbird.png')

    # Definir o kernel 9x9
    # kernel = [
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ]

    # Aplicar a correlação com o kernel na imagem
    # imagem_PorcoCorrelacao = imagem_Porco.correlacao(kernel)

    # Salvar a imagem resultante
    # imagem_PorcoCorrelacao.salvar('pigbird_correlacao.png')

    # imagem_PorcoCorrelacao.mostrar()

    # Questão Gato borrado

    # imagem_gato = Imagem.carregar('test_images/cat.png')
    # imagem_Gatoborrada = imagem_gato.borrada(5)
    # imagem_Gatoborrada.salvar('cat_borrado.png')
    # imagem_Gatoborrada.mostrar()

    # Questão 5- Python com nitidez

    # imagem_python = Imagem.carregar('test_images/python.png')
    # imagem_Pythonnitida = imagem_python.focada(11)
    # imagem_Pythonnitida.salvar('python_nitida.png')
    # imagem_Pythonnitida.mostrar()

    # Parte Escrita:
    # Resultado final do kernel para a operação de nitidez:
    # Este kernel representa a combinação dos elementos necessários para realizar a operação de nitidez em uma única correlação.
    # Cada elemento da matriz representa a contribuição do pixel original (I) multiplicada por 2, subtraída do valor do pixel
    # na mesma posição da imagem borrada (B), conforme descrito pela fórmula Sx,y = round(2 * Ix,y - Bx,y).
    # Portanto, o resultado final do kernel para a operação de nitidez é:
    # [[-1/9, -1/9, -1/9],
    #  [-1/9, 17/9, -1/9],
    #  [-1/9, -1/9, -1/9]]

    # Esta matriz representa a combinação dos seguintes elementos:
    # 1. Multiplicação do pixel original por 2:
    #    [[2, 2, 2],
    #     [2, 2, 2],
    #     [2, 2, 2]]

    # 2. Subtração do valor do pixel na mesma posição da imagem borrada:
    #    [[2 - Bx,y, 2 - Bx,y, 2 - Bx,y],
    #     [2 - Bx,y, 2 - Bx,y, 2 - Bx,y],
    #     [2 - Bx,y, 2 - Bx,y, 2 - Bx,y]]
    # Dividir cada elemento da matriz resultante por 9 para normalizar e obter o kernel final para a operação de nitidez.

    # Questão 6- Contrução com bordas

    # imagem_construcao = Imagem.carregar('test_images/construct.png')
    # imagem_Construcaobordas = imagem_construcao.bordas()
    # imagem_Construcaobordas.salvar('construct_bordas.png')
    # imagem_Construcaobordas.mostrar()

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
