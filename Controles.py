import pygame as pg

pg.init()

LARGURA, ALTURA = (500, 400)

gameloop = True

tela = pg.display.set_mode((LARGURA, ALTURA))


class Controles:
    MODELO_BOTOES = ("cir", "ret")
    botoes = list()
    
    def __init__(self, tela):
        self.tela = tela
    
    def novo_botao(
        self,
        id, 
        rect = None,
        cor = (0, 20, 100),
        formato = "cir",
        pos_xy = (0, 0),
        radius = 100
    ):
        if formato in self.MODELO_BOTOES:
            if formato == self.MODELO_BOTOES[0]:
                botao_atual = pg.draw.circle(
                    surface = self.tela,
                    color= cor,
                    center = pos_xy,
                    radius = radius
                )
            elif formato == self.MODELO_BOTOES[1]:
                botao_atual = pg.draw.rect(
                    surface = self.tela,
                    color = cor,
                    rect = rect,
                    border_radius = radius
                )
            self.botoes.append({id: botao_atual})
        else:
            raise ValueError(f"\"{formato}\" não é um MODELO válido.")
    
    def verificar_clique(self, id_botao) -> bool:
        estado_mouse = pg.mouse.get_pressed()
        pos_mouse = pg.mouse.get_pos()
        if estado_mouse[0]:
            # pegando o estado do primeiro botão do mouse
            for botao in self.botoes:
                if id_botao in botao:
                    # verificando colisao do clique com o botão
                    return botao[id_botao].collidepoint(pos_mouse)
                    # print(f"Estou clicando no botão {id_botao}? ", botao[id_botao].collidepoint(pos_mouse))
            

if __name__ == "__main__":
    c1 = Controles(tela)
    
    x, y = [400, 100]
    velocidade = 2
    
    tamanho_normal = 80
    tamanho_extra = 1
    tamanho_atual = tamanho_normal
    
    while gameloop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameloop = False
        tela.fill((30, 80, 100))
        
        bola = pg.draw.circle(tela, (200, 200, 50), (x, y), tamanho_atual)
        
        c1.novo_botao(id = "botao_esq", pos_xy = (80, 800), radius = 80)
        c1.novo_botao(id = "botao_dir", pos_xy = (300, 800), radius = 80)
        c1.novo_botao(id = "botao_cim", pos_xy = (190, 680), radius = 80)
        c1.novo_botao(id = "botao_bai", pos_xy = (190, 920), radius = 80)
        
        c1.novo_botao(id = "botao_expandir", pos_xy = (2000, 800), radius = 90, cor = (0, 200, 0))
        
        # c1.novo_botao(id = "botao_teste2", formato = "ret", rect = (200, 200, 250, 100), radius = 50)
        
        if c1.verificar_clique("botao_esq"):
            x -= velocidade
        elif c1.verificar_clique("botao_dir"):
            x += velocidade
        if c1.verificar_clique("botao_cim"):
            y -= velocidade
        elif c1.verificar_clique("botao_bai"):
            y += velocidade
        
        if c1.verificar_clique("botao_expandir"):
            tamanho_atual += tamanho_extra
        else:
            tamanho_atual = tamanho_normal
        
        pg.display.flip()

