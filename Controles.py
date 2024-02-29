import pygame as pg
from random import randint

pg.init()

LARGURA, ALTURA = (920, 540)

gameloop = True

tela = pg.display.set_mode((LARGURA, ALTURA))


class Controles:
    MODELO_BOTOES = ("cir", "ret")
    botoes = dict()
    
    def __init__(self, tela):
        self.tela = tela
    
    def novo_botao(
        self,
        id_botao,
        id_categoria, 
        rect = None,
        cor = (0, 20, 100),
        formato = "cir",
        pos_xy = (0, 0),
        radius = 100
    ):
        if formato in self.MODELO_BOTOES:
            """if formato == self.MODELO_BOTOES[0]:
                botao_atual = pg.draw.circle(
                    surface = self.tela,
                    color= cor,
                    center = pos_xy,
                    radius = radius
                )
                print(botao_atual)
            elif formato == self.MODELO_BOTOES[1]:
                botao_atual = pg.draw.rect(
                    surface = self.tela,
                    color = cor,
                    rect = rect,
                    border_radius = radius
                )"""
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
            if id_botao == k and estado_mouse[0]:
                if v["status"]:
                    return v["status"]
                # verificando colisao do clique com o botão
                if v["rect_botao"].collidepoint(pos_mouse):
                    for chave, valor in self.botoes.items():
                        if chave != k:
                            # definindo o status de todos os outros botões da mesma categoria  do botão atual como False
                            if self.botoes[chave]["categoria"] == v["categoria"]:
                                self.botoes[chave]["status"] = False
                    # definindo o status do botão ativo para True
                    self.botoes[k]["status"] = True
                    return self.botoes[k]["status"]
                # print(f"Estou clicando no botão {id_botao}? ", botao[id_botao].collidepoint(pos_mouse))"""
            else:
                # definindo o status de todos os botões da mesma categoria para False
                for k, v in self.botoes.items():
                    if v["categoria"] == self.botoes[id_botao]["categoria"]:
                        self.botoes[k]["status"] = False
    
    def _desenhar_botoes(self):
        for k, v in self.botoes.items():
            if v["formato"] == self.MODELO_BOTOES[0]:
                # desenhando botão do formato de circulo
                pg.draw.circle(
                    surface = self.tela,
                    color = v["cor"],
                    center = (
                        v["rect_botao"][0] + (v["rect_botao"][-1] // 2),
                        v["rect_botao"][1] + (v["rect_botao"][-1] // 2)
                    ),
                    radius = v["rect_botao"][-1] // 2
                )
            elif v["formato"] == self.MODELO_BOTOES[1]:
                # desenhando botão do formato retângulo
                pg.draw.rect(self.tela, v["cor"], v["rect_botao"])
    
    def atualizar(self):
        self._desenhar_botoes()
    
    def set_status_botao(self, id, status):
        if id in self.botoes.keys():
            self.botoes[id]["status"] = status
        else:
            raise ValueError(f"\"{id}\" não é um id de botão válido.")
    
    @staticmethod
    def cor_aleatoria(min = 0, max = 255) -> list:
        cor = list()
        for c in range(3):
            cor.append(randint(min, max))
        return cor


if __name__ == "__main__":
    c1 = Controles(tela)
    c2 = Controles(tela)
    c3 = Controles(tela)
    
    x, y = [400, 100]
    velocidade = 2
    
    # tamanho_normal = 80
    tamanho_normal = 40
    tamanho_extra = 1
    tamanho_atual = tamanho_normal
    
    c1.novo_botao(
        id_botao = "botao_esq",
        id_categoria = "movimento",
        # pos_xy = (80, 800),
        pos_xy = (80, 400),
        radius = 35
    )
    
    c1.novo_botao(
        id_botao = "botao_dir",
        id_categoria = "movimento",
        # pos_xy = (300, 800),
        pos_xy = (190, 400),
        radius = 35
    )
    
    c1.novo_botao(
        id_botao = "botao_cim",
        id_categoria = "movimento",
        # pos_xy = (190, 680),
        pos_xy = (135, 340),
        radius = 35
    )
    
    c1.novo_botao(
        id_botao = "botao_bai",
        id_categoria = "movimento",
        # pos_xy = (190, 920),
        pos_xy = (135, 460),
        radius = 35
    )
    
    c2.novo_botao(
        id_botao = "botao_expandir",
        id_categoria = "poder1",
        pos_xy = (2000, 800),
        radius = 90,
        cor = (0, 200, 0)
    )
    
    c3.novo_botao(
        id_botao = "disparar",
        id_categoria = "arma1",
        pos_xy = (800, 400),
        radius = 50,
        cor = (100, 0, 0)
    )
    
    rect_bala = None
    bala_x = x
    bala_y = y
    bala_visivel = False
    velocidade_bala = 20
    indicador_xy = [40, 0]
    
    while gameloop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameloop = False
        tela.fill((30, 80, 100))
        c1.atualizar()
        
        bola = pg.draw.circle(tela, (200, 200, 50), (x, y), tamanho_atual)
        indicador = pg.draw.circle(tela, (200, 0, 0), (x + indicador_xy[0], y + indicador_xy[1]), 2)
        
        # c1.novo_botao(id = "botao_teste2", formato = "ret", rect = (200, 200, 250, 100), radius = 50)
        
        if c1.verificar_clique("botao_esq"):
            x -= velocidade
            if not bala_visivel:
                indicador_xy[0] = -40
                indicador_xy[1] = 0
        elif c1.verificar_clique("botao_dir"):
            x += velocidade
            if not bala_visivel:
                indicador_xy[0] = 40
                indicador_xy[1] = 0
        if c1.verificar_clique("botao_cim"):
            y -= velocidade
            if not bala_visivel:
                indicador_xy[0] = 0
                indicador_xy[1] = -40
        elif c1.verificar_clique("botao_bai"):
            y += velocidade
            if not bala_visivel:
                indicador_xy[0] = 0
                indicador_xy[1] = 40
        
        if c3.verificar_clique("disparar"):
            bala_visivel = True
            print("disparado")
        
        if bala_visivel:
            if bala_x >= LARGURA:
                bala_x = x + indicador_xy[0]
                bala_visivel = False
            elif bala_x <= 0:
                bala_x = x + indicador_xy[0]
                bala_visivel = False
            elif bala_y <= 0:
                bala_y = y + indicador_xy[1]
                bala_visivel = False
            elif bala_y >= ALTURA:
                bala_y = y + indicador_xy[1]
                bala_visivel = False
            else:
                if indicador_xy[0] > 0:
                    bala_x += velocidade_bala
                elif indicador_xy[0] < 0:
                    bala_x -= velocidade_bala
                elif indicador_xy[1] < 0:
                    bala_y -= velocidade_bala
                elif indicador_xy[1] > 0:
                    bala_y += velocidade_bala
            rect_bala = pg.draw.circle(tela, Controles.cor_aleatoria(), (bala_x, bala_y), 5)
        else:
            bala_x = x + indicador_xy[0]
            bala_y = y + indicador_xy[1]
        
        if c2.verificar_clique("botao_expandir"):
            tamanho_atual += tamanho_extra
        else:
            tamanho_atual = tamanho_normal
        
        pg.display.flip()

