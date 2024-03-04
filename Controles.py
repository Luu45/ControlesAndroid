import pygame as pg
from random import randint

pg.init()

LARGURA, ALTURA = (2265, 1040)

gameloop = True

tela = pg.display.set_mode((LARGURA, ALTURA))


class Controles:
    """
        Atributos do método de criação de botões
    """
    MODELO_BOTOES = ("cir", "ret")
    botoes = dict()
    
    """
        Atributos do método de efeitos dos botões
    """
    EFEITO_BOTOES = ("expansao", "pulsacao")
    
    def __init__(self, tela):
        self.tela = tela
        self.expansao = 0
        self.botao_expansao = None
    
    def novo_botao(
        self,
        id_botao,
        id_categoria, 
        rect = None,
        cor = (0, 20, 100),
        formato = "cir",
        pos_xy = (0, 0),
        radius = 100
    ) -> None:
        if formato in self.MODELO_BOTOES:
            # caso o formato do botão seja cir(circulo)
            if formato == self.MODELO_BOTOES[0]:
                self.botoes[id_botao] = {
                    "rect_botao": pg.Rect(
                        pos_xy[0] - radius,
                        pos_xy[1] - radius,
                        radius * 2,
                        radius * 2
                    ),
                    "status": False,
                    "formato": formato,
                    "cor": cor,
                    "categoria": id_categoria
                }
            # caso o formato do botão seja ret(retangulo)
            elif formato == self.MODELO_BOTOES[1]:
                self.botoes[id_botao] = {
                    "rect_botao": rect,
                    "status": False,
                    "formato": formato,
                    "cor": cor,
                    "categoria": id_categoria
                }
        else:
            raise ValueError(f"\"{formato}\" não é um MODELO válido.")
    
    def verificar_clique(self, id_botao) -> bool:
        estado_mouse = pg.mouse.get_pressed()
        pos_mouse = pg.mouse.get_pos()
        for k, v in self.botoes.items():
            for k2, v2 in self.botoes.items():
                # definindo todos os demais botões da mesma categoria atual como False
                if k2 != id_botao and self.botoes[id_botao]["categoria"] == v2["categoria"]:
                    self.botoes[id_botao]["status"] = False
            # caso o id do botão seja igual ao id atual e também esteja
            # com mouse pressionado na tela
            if id_botao == k:
                if estado_mouse[0]:
                    print(k)
                    # caso o clique esteja colidindo com o botão atual
                    if v["rect_botao"].collidepoint(pos_mouse):
                        self.botoes[k]["status"] = True
                        return True
                    else:
                        return False
    
    def efeitos(
        self,
        superficie,
        efeito,
        id_categoria_botao,
        cor_expansao = (0, 255, 0),
        tamanho_expansao = 5,
        velocidade_expansao = 0.3
    ):
        # caso o efeito seja o efeito de expansao
        if self.EFEITO_BOTOES[0] == efeito:
            estado_mouse = pg.mouse.get_pressed()[0]
            # quando o botão for solto volta a expansao a zero
            if not estado_mouse:
                self.expansao = 0
                
            for k, info_botao in self.botoes.items():
                # caso a categoria seja a categoria indicada
                if info_botao["categoria"] == id_categoria_botao:
                    # caso o botão atual esteja ativo
                    if info_botao["status"]:
                        # caso a expansão não esteja no nível máximo some a 
                        # velocidade a seu valor atual
                        if int(self.expansao) <= tamanho_expansao:
                            self.expansao += velocidade_expansao
                        
                        # dando o primeiro valor do botão inicial da expansao
                        if self.botao_expansao is None:
                            self.botao_expansao = k
                        
                        # caso o botao de expansao for diferente do botao pressionado
                        # atualmente zera o nivel de expansao e atualiza o botao que sofrerá 
                        # a expansao
                        if self.botao_expansao != k:
                            self.expansao = 0
                            self.botao_expansao = k
                        
                        # caso o formato seja o formato circular
                        if info_botao["formato"] == self.MODELO_BOTOES[0]:
                            pg.draw.circle(
                                surface = superficie,
                                color = cor_expansao,
                                center = (
                                    info_botao["rect_botao"][0] + info_botao["rect_botao"][2] // 2,
                                    info_botao["rect_botao"][1] + info_botao["rect_botao"][2] // 2),
                                radius = info_botao["rect_botao"][2] // 2 + self.expansao
                            )
                        elif info_botao["formato"] == Controles.MODELO_BOTOES[1]:
                            print("botao roupas")
                            pg.draw.rect(
                                surface = superficie,
                                color = cor_expansao,
                                rect = (
                                    info_botao["rect_botao"][0],
                                    info_botao["rect_botao"][1],
                                    info_botao["rect_botao"][2] + self.expansao,
                                    info_botao["rect_botao"][3] + self.expansao
                                )
                            )
                        
        elif self.EFEITO_BOTOES[1]:
            ...
    
    def _desenhar_botoes(self):
        for k, v in self.botoes.items():
            # desenhando botão do formato de circulo
            if v["formato"] == self.MODELO_BOTOES[0]:
                pg.draw.circle(
                    surface = self.tela,
                    color = v["cor"],
                    center = (
                        v["rect_botao"][0] + (v["rect_botao"][-1] // 2),
                        v["rect_botao"][1] + (v["rect_botao"][-1] // 2)
                    ),
                    radius = v["rect_botao"][-1] // 2
                )
            # desenhando botão do formato retângulo
            elif v["formato"] == self.MODELO_BOTOES[1]:
                pg.draw.rect(
                    surface = self.tela,
                    color = v["cor"],
                    rect = v["rect_botao"]
                )
    
    def atualizar(self):
        self._desenhar_botoes()
    
    def set_status_botao(self, id, status):
        if id in self.botoes.keys():
            self.botoes[id]["status"] = status
        else:
            raise ValueError(f"\"{id}\" não é um id de botão válido.")
    
    def get_status_botao(self, id) -> bool:
        if id in self.botoes.keys():
            return self.botoes[id_botao]["status"]
        else:
            raise ValueError(f"\"{id}\" não é um id de botão válido.")
    
    @staticmethod
    def cor_aleatoria(min = 0, max = 255) -> list:
        cor = list()
        for c in range(3):
            cor.append(randint(min, max))
        return cor


def anima_sprite(spritesheet, dimensao, x, y, rect_sprite, index_xy):
    janela = pg.Surface(rect_sprite[2:])
    spritesheet = pg.transform.scale(spritesheet, dimensao)
    tela.blit(
        spritesheet,
        (x, y),
        (
            rect_sprite[0] + index_xy[0] * rect_sprite[2],
            rect_sprite[1] + index_xy[1] * rect_sprite[3],
            rect_sprite[2],
            rect_sprite[3]
        )
    )


if __name__ == "__main__":
    c1 = Controles(tela)
    c2 = Controles(tela)
    c3 = Controles(tela)
    
    # posição inicial do Adany
    x, y = [500, 550]
    # velocidade do Adany
    velocidade = 1
    # velocidade da animação do Adany
    velocidade_animacao = 0.2
    
    tamanho_normal = 80
    tamanho_extra = 1
    tamanho_atual = tamanho_normal
    
    # tamanho base dos botões de movimento
    tamanho_botoes = 70
    
    c1.novo_botao(
        id_botao = "botao_esq",
        id_categoria = "movimento",
        pos_xy = (80, 800),
        radius = tamanho_botoes
    )
    
    c1.novo_botao(
        id_botao = "botao_dir",
        id_categoria = "movimento",
        pos_xy = (300, 800),
        radius = tamanho_botoes
    )
    
    c1.novo_botao(
        id_botao = "botao_cim",
        id_categoria = "movimento",
        pos_xy = (190, 680),
        radius = tamanho_botoes
    )
    
    c1.novo_botao(
        id_botao = "botao_bai",
        id_categoria = "movimento",
        pos_xy = (190, 920),
        radius = tamanho_botoes
    )
    
    c2.novo_botao(
        id_botao = "botao_expandir",
        id_categoria = "poder1",
        pos_xy = (2000, 800),
        cor = (0, 0, 100)
    )
    
    c3.novo_botao(
        id_botao = "roupas",
        id_categoria = "armadura",
        rect = (1000, 900, 200, 100),
        formato = "ret",
        cor = (0, 0, 100)
    )
    
    adany = pg.image.load("adao_spritesheet.png")
    
    index_x = 0
    index_y = 0
    
    fundo = pg.image.load("painel 1.jpg")
    fundo = pg.transform.scale(fundo, (LARGURA, ALTURA))
    
    while gameloop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameloop = False
        tela.fill((30, 80, 100))
        # fundo
        tela.blit(fundo, (0, 0))
        
        # Adany
        anima_sprite(
            spritesheet = adany,
            dimensao = (1400, 900),
            x = int(x),
            y = int(y),
            rect_sprite = (0, 0, 156, 224),
            index_xy = (int(index_x), index_y)
        )
        # atualização dos botões
        c1.atualizar()
        
        c1.efeitos(
            superficie = tela,
            efeito = "expansao",
            id_categoria_botao = "movimento",
            cor_expansao = (0, 0, 200),
            tamanho_expansao = 7
        )
        
        c2.efeitos(
            superficie = tela,
            efeito = "expansao",
            id_categoria_botao = "poder1",
            cor_expansao = (0, 0, 200),
            tamanho_expansao = 10
        )
        
        # bola = pg.draw.circle(tela, (200, 200, 50), (x, y), tamanho_atual)
        for info in c1.botoes.values():
            if info["categoria"] == "movimento":
                if info["status"]:
                    if int(index_x) < 8:
                        index_x += velocidade_animacao
                    else:
                        index_x = 1
                elif not pg.mouse.get_pressed()[0]:
                    index_x = 0
        
        # c1.novo_botao(id = "botao_teste2", formato = "ret", rect = (200, 200, 250, 100), radius = 50)
        
        if c1.verificar_clique("botao_esq"):
            index_y = 1
            x -= velocidade
        elif c1.verificar_clique("botao_dir"):
            index_y = 3
            x += velocidade
            
        if c1.verificar_clique("botao_cim"):
            index_y = 0
            y -= velocidade
        elif c1.verificar_clique("botao_bai"):
            index_y = 2
            y += velocidade
        
        c2.verificar_clique("botao_expandir")
        
        """if c2.verificar_clique("botao_expandir"):
            tamanho_atual += tamanho_extra
        else:
            tamanho_atual = tamanho_normal"""
        
        pg.display.flip()

