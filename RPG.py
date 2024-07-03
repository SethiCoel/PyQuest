import os
from random import randint, choice
from time import sleep
import keyboard
import sqlite3



class RPG:
    def __init__(self):
        self.banco_dados()
        self.player_status()
        self.goblin_status()
        self.goblin_xama_status()
        self.velocidade_combate = 1
        self.velocidade_texto = 0.7
    
    
    def __str__(self):
        pass
    
    
    def banco_dados(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()


#////////// Dados para as tabelas /////////////////////////////////////
          
        # jogador
        player_nome = 'Player'
        player_nivel = 1
        player_vida = 20
        player_dano = 3
        player_xp = 0
        player_vida_padrao = 20
        player_dano_padrao = 3
        ultima_posicao = 0

        #UP do jogador
        taxa_aumento_vida = 1.1
        taxa_aumento_dano = 1
        taxa_proximo_nivel = 1.4
        xp_necessario = 20


        # goblin
        goblin_nome = 'Goblin'
        goblin_vida = 16
        goblin_dano_fraco = 2
        goblin_dano_medio = 3
        goblin_dano_forte = 4
        goblin_dano_critico = 6


        # goblin Xamã
        goblin_xama_nome = 'Goblin Xamã'
        goblin_xama_vida = 40
        goblin_xama_dano_fraco = 4
        goblin_xama_dano_medio = 6
        goblin_xama_cura = 8
        goblin_xama_dano_critico = 7

#////////// criando a tabela do jogador //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
        nome TEXT,
        nivel INTEGER,
        vida INTEGER,
        dano INTEGER,
        xp INTEGER,
        vida_padrao INTEGER,
        dano_padrao INTEGER,
        taxa_vida INTEGER,
        taxa_dano INTEGER,
        taxa_proximo_nivel INTEGER,
        xp_necessario INTEGER,
        ultima_posicao INTEGER
        )
    ''')

#////////// criando a tabela monstro ativo //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS monstro_ativo (nome TEXT)''')
        
        monstro_ativo = self.cursor.execute('''
        SELECT nome FROM monstro_ativo
    ''').fetchone()

        if monstro_ativo is None:
           self.cursor.execute('''
            INSERT INTO monstro_ativo (nome)
            VALUES ('vazio')
            ''') 
        
#////////// criando a tabela do goblin  //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS goblin (
        nome TEXT,
        vida INTEGER,
        dano_fraco INTEGER,
        dano_medio INTEGER,
        dano_forte INTEGER,
        dano_critico INTEGER,
        vida_padrao INTEGER
        )
    ''')

#////////// criando a tabela do goblin xamã  //////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS goblin_xama (
        nome TEXT,
        vida INTEGER,
        dano_fraco INTEGER,
        dano_medio INTEGER,
        cura INTEGER,
        dano_critico INTEGER,
        vida_padrao INTEGER
        )
    ''')

#////////// criando a tabela de itens //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,   
        tipo TEXT,
        dano INTEGER,
        beneficio INTEGER,
        equipado TEXT          
        )
    ''')
        
#////////// criando o inventario do jogador //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        dano INTEGER,
        beneficio INTEGER,
        equipado TEXT   
        )
    ''')

#////////// conferindo os dados de todas as tabelas //////////////////////////////    
        conferir_dados_player = self.cursor.execute('''
        SELECT * FROM player
    ''').fetchone()
        
        conferir_dados_itens = self.cursor.execute('''
        SELECT * FROM itens
    ''').fetchone()

        conferir_dados_inventario = self.cursor.execute('''
        SELECT * FROM inventario
    ''').fetchone()
        
        conferir_dados_goblin = self.cursor.execute('''
        SELECT * FROM goblin
    ''').fetchone()

        conferir_dados_goblin_xama = self.cursor.execute('''
        SELECT * FROM goblin_xama
    ''').fetchone()
        
#////////// adicionando dados a tabela do jogador //////////////////////////////
        if conferir_dados_player is None:
            self.cursor.execute(f'''
            INSERT INTO player (nome, nivel, vida, dano, xp, vida_padrao, dano_padrao,
            taxa_vida, taxa_dano, taxa_proximo_nivel, xp_necessario, ultima_posicao) 
            VALUES (
            '{player_nome}', {player_nivel}, {player_vida}, 
            {player_dano}, {player_xp}, {player_vida_padrao}, 
            {player_dano_padrao}, {taxa_aumento_vida},{taxa_aumento_dano},
            {taxa_proximo_nivel}, {xp_necessario}, {ultima_posicao}
            )                                           
        ''')
        
#////////// adicionando dados a tabela de itens //////////////////////////////
        if conferir_dados_itens is None:
            self.cursor.execute('''
            INSERT INTO itens (nome, tipo, dano, beneficio, equipado)
            VALUES
            ('Caliburn', 'Espada', 2, NULL, '[ ]'),
            ('Elixir', 'Poção de Cura', NULL, 20, '[ ]')      
        ''')
            
#/////////// adicionando dados a tabela goblin ////////////////////////////////
        if conferir_dados_goblin is None:
            self.cursor.execute(f'''
            INSERT INTO goblin (nome, vida, dano_fraco, dano_medio, dano_forte, dano_critico, vida_padrao)
            VALUES ('{goblin_nome}', {goblin_vida}, {goblin_dano_fraco},
            {goblin_dano_medio}, {goblin_dano_forte}, {goblin_dano_critico}, {goblin_vida})
        ''')
            
#/////////// adicionando dados a tabela goblin xamã ////////////////////////////////
        if conferir_dados_goblin_xama is None:
            self.cursor.execute(f'''
            INSERT INTO goblin_xama (nome, vida, dano_fraco, dano_medio, cura, dano_critico, vida_padrao)
            VALUES ('{goblin_xama_nome}', {goblin_xama_vida}, {goblin_xama_dano_fraco},
            {goblin_xama_dano_medio}, {goblin_xama_cura}, {goblin_xama_dano_critico}, {goblin_xama_vida})
    	''')

#////////// adicionando dados a tabela inventário do jogador //////////////////////////////     
        if conferir_dados_inventario is None:
            self.cursor.execute('''
                INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                SELECT nome, tipo, dano, beneficio, equipado
                FROM itens WHERE id = 2
            ''') #ELIXIR

            # self.cursor.execute('''
            #     INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
            #     SELECT nome, tipo, dano, beneficio, equipado
            #     FROM itens WHERE id = 1
            # ''')

            # self.cursor.execute('''
            #     INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
            #     SELECT nome, tipo, dano, beneficio, equipado
            #     FROM itens WHERE id = 1
            # ''')

        self.conn.commit()

#//////////////////////////////////////////////////////////////////////////////
    def player_status(self):
        self.player_nome = self.cursor.execute('''
        SELECT nome FROM player ''').fetchone()[0]

        self.player_nivel = self.cursor.execute('''
        SELECT nivel FROM player ''').fetchone()[0]

        self.player_vida = self.cursor.execute('''
        SELECT vida FROM player ''').fetchone()[0]

        self.player_dano = self.cursor.execute('''
        SELECT dano FROM player ''').fetchone()[0]
        
        self.player_xp = self.cursor.execute('''
        SELECT xp FROM player ''').fetchone()[0]

        self.vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM player ''').fetchone()[0]

        self.xp_necessario = self.cursor.execute('''
        SELECT xp_necessario FROM player ''').fetchone()[0]

        self.player_ficha = f'''{self.player_nome}: {'█' * int(self.player_vida)} {' ' * int(self.vida_padrao - self.player_vida)} | {self.player_vida:.0f}/{self.vida_padrao:.0f} 
Dano: {self.player_dano:.0f} {' ' * int(self.vida_padrao)}   Nível: {self.player_nivel}
EXP: {self.player_xp:.0f}/{self.xp_necessario:.0f}
    '''

#//////////////////////////////////////////////////////////////////////////////
    def goblin_status(self):
        self.goblin_nome = self.cursor.execute('''
        SELECT nome FROM goblin ''').fetchone()[0]

        self.goblin_vida = self.cursor.execute('''
        SELECT vida FROM goblin ''').fetchone()[0]

        self.goblin_dano_fraco = self.cursor.execute('''
        SELECT dano_fraco FROM goblin ''').fetchone()[0]

        self.goblin_dano_medio = self.cursor.execute('''
        SELECT dano_medio FROM goblin ''').fetchone()[0]

        self.goblin_dano_forte = self.cursor.execute('''
        SELECT dano_forte FROM goblin ''').fetchone()[0]

        self.goblin_dano_critico = self.cursor.execute('''
        SELECT dano_critico FROM goblin''').fetchone()[0]

        self.goblin_vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM goblin ''').fetchone()[0]

        self.goblin_ficha = f'{self.goblin_nome}: {'█' * int(self.goblin_vida)} {' ' * int(self.goblin_vida_padrao - self.goblin_vida)} | {self.goblin_vida:.0f}/{self.goblin_vida_padrao}'

#//////////////////////////////////////////////////////////////////////////////
    def goblin_xama_status(self):
        self.goblin_xama_nome = self.cursor.execute('''
        SELECT nome FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_vida = self.cursor.execute('''
        SELECT vida FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_dano_fraco = self.cursor.execute('''
        SELECT dano_fraco FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_dano_medio = self.cursor.execute('''
        SELECT dano_medio FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_cura = self.cursor.execute('''
        SELECT cura FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_dano_critico = self.cursor.execute('''
        SELECT dano_critico FROM goblin_xama ''').fetchone()[0]

        self.goblin_xama_vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM goblin_xama ''').fetchone()[0]


        self.goblin_xama_ficha = f'{self.goblin_xama_nome}: {'█' * int(self.goblin_xama_vida)} {' ' * int(self.goblin_xama_vida_padrao - self.goblin_xama_vida)} | {self.goblin_xama_vida:.0f}/{self.goblin_xama_vida_padrao}'

#//////////////////////////////////////////////////////////////////////////////
    def inventario(self):
        RPG.limpar_tela()
        
        

        jogador_vida = self.cursor.execute('''
        SELECT vida FROM player
        ''').fetchone()[0]

        jogador_vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM player
        ''').fetchone()[0]

        self.itens = self.cursor.execute('''
        SELECT * FROM inventario
        ''').fetchall()

        posicao_itens = []
        item_ids = []

        tamanho_hud = 30

        RPG.titulo('Inventário')

        RPG.cor(f'{self.player_ficha}\n')


        RPG.cor(f'╔{'═' * (tamanho_hud - 2)}╗', 'amarelo')
       

        for num, item in enumerate(self.itens):
            indice = num + 1
            
            item_ids.append(item[0])

            posicao_itens.append(str(indice))

            RPG.cor(f'''║({indice}) {item[1].ljust(tamanho_hud - 15)} {item[5].ljust(tamanho_hud - 22)}║''', 'amarelo')

        RPG.cor(f'╚{'═' * (tamanho_hud - 2)}╝', 'amarelo')
        
        print('ESC voltar')
        
        listar_itens = RPG.teclas_inventario()

#//////////////////////////////////////////////////////////////////////////////
        if listar_itens in posicao_itens:
            self.item_especifico = self.itens[int(listar_itens) - 1]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Caliburn':

                verificar_se_tem_algo_equipado = self.cursor.execute(f'''
                SELECT id FROM inventario WHERE equipado = '[*]' 
                ''').fetchone()

                self.caliburn()

                print('(1) Equipar/Desequipar')
                print('(2) Descartar')
                

                print('\nESC Voltar')

                acao = RPG.tecla_acao()

                
                if acao == '1':
                    self.player_status()

                    self.cursor.execute('''
                    SELECT * FROM inventario''')


                    if verificar_se_tem_algo_equipado is not None:

                        if item_ids[int(listar_itens)-1] != verificar_se_tem_algo_equipado[0]:

                            RPG.frase('\nUm outro item ja está equipado!', 'vermelho')
                            sleep(self.velocidade_texto)
                            self.inventario()

                    if verificar_se_tem_algo_equipado is None:
                            
                        self.cursor.execute(f'''
                        UPDATE player SET dano = dano_padrao + {self.item_especifico[3]}''')
                        
                        self.cursor.execute(f'''
                        UPDATE inventario SET equipado = '[*]'
                        WHERE id = {item_ids[int(listar_itens)-1]}   
                        ''')
                        
                        self.conn.commit()

                        RPG.frase(f'\n{self.item_especifico[1]} equipada!', 'verde')
                        sleep(self.velocidade_texto)


                    elif verificar_se_tem_algo_equipado[0] == item_ids[int(listar_itens)-1]:

                        self.cursor.execute(f'''
                        UPDATE player SET dano = dano_padrao ''')

                        self.cursor.execute(f'''
                        UPDATE inventario SET equipado = '[ ]'
                        WHERE id = {item_ids[int(listar_itens)-1]} 
                        ''')

                        self.conn.commit()
                        
                        RPG.frase(f'\n{self.item_especifico[1]} desequipada!', 'amarelo')
                        sleep(self.velocidade_texto)

                        
                
                if acao == '2':

                    if verificar_se_tem_algo_equipado[0] == item_ids[int(listar_itens)-1]:
                        self.cursor.execute(f'''
                        UPDATE player SET dano = dano_padrao''')
                    
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')

                    self.conn.commit()

                    RPG.frase('Caliburn descartada!', 'vermelho')
                    sleep(self.velocidade_texto)

                if acao == 'esc':
                    self.inventario()

                self.inventario()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Elixir':
                cura_elixir = self.cursor.execute('''
                SELECT beneficio FROM itens WHERE id = 2
                ''').fetchone()[0] 
                
                
                self.elixir()

                print('(1) Usar')
                print('(2) Descartar')
                
                print('\nESC Voltar')

                acao = RPG.tecla_acao()

                if acao == '1':

                    if jogador_vida < jogador_vida_padrao:
                        self.cursor.execute(f'''
                        UPDATE player SET vida = vida + {cura_elixir}
                        ''')                        
                        self.conn.commit()
                        RPG.frase('\nElixir usado!', 'verde')
                        sleep(self.velocidade_texto)

                        self.cursor.execute(f'''
                        DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                        ''')
                        
                        self.conn.commit()
                        
                        jogador_vida = self.cursor.execute('''
                        SELECT vida FROM player
                        ''').fetchone()[0]

                        if jogador_vida > jogador_vida_padrao:
                                self.cursor.execute(f'''
                                UPDATE player SET vida = vida_padrao
                                ''')
                                self.conn.commit()
                        
                    elif jogador_vida == jogador_vida_padrao:
                        RPG.frase('\nSua vida está cheia!', 'vermelho')
                        sleep(self.velocidade_texto)  

                    
                if acao == '2':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')
                    self.conn.commit()

                    RPG.frase('\nElixir descartado!', 'vermelho')
                    sleep(self.velocidade_texto)

                if acao == 'esc':
                    self.inventario()
                
                self.inventario()

        if listar_itens == 'esc':
            self.monstro_ativo()
        
        if not listar_itens in posicao_itens:
            self.inventario()

#////////////////////////////////////////////////////////////////////////////// 
    def elixir(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[1]

        nome = item_especifico[1]
        tipo = item_especifico[2]
        cura = item_especifico[4]
        
        RPG.hud_item(nome, tipo, f'{cura} de cura')
        
#//////////////////////////////////////////////////////////////////////////////        
    def caliburn(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[0]

        nome = item_especifico[1]
        tipo = item_especifico[2]
        dano = item_especifico[3]
        
        RPG.hud_item(nome, tipo, f'{dano} de dano')

    def hud_item(nome, tipo, efeito):
        
        tamanho_hud = 30
        
        nome_centralizado = nome.center(tamanho_hud - 2)
        
        tipo_formatado = f"Tipo: {tipo}".ljust(tamanho_hud - 3)
        efeito_formatado = f"Efeito: {efeito}".ljust(tamanho_hud - 3)
        
        
        hud = f"""╔{'═' * (tamanho_hud - 2)}╗
║{nome_centralizado}║
╠{'═' * (tamanho_hud - 2)}╣
║ {tipo_formatado}║
║ {efeito_formatado}║
╚{'═' * (tamanho_hud - 2)}╝
"""
        RPG.cor(hud,'amarelo')

    def titulo(titulo, cor=''):
        tamanho_hud = 20
        
        titulo_centralizado = titulo.center(tamanho_hud - 2)
        
        
        hud = f"""╔{'═' * (tamanho_hud - 2)}╗
║{titulo_centralizado}║
╚{'═' * (tamanho_hud - 2)}╝
"""     
        if cor == '':
            RPG.cor(hud,'amarelo')
        
        else:
            RPG.cor(hud, cor)

    def frase(texto, cor='', texto2='', cor2='', vel=''):
        if cor == 'vermelho':
            cor = '\033[0;31;40m'
        elif cor == 'verde':
            cor = '\033[0;32;40m'
        elif cor == 'amarelo':
            cor = '\033[0;33;40m'
        elif cor == 'azul':
            cor = '\033[0;34;40m'
        elif cor == 'ciano':
            cor = '\033[0;36;40m'
        else:
            cor = ''

        if cor2 == 'vermelho':
            cor2 = '\033[0;31;40m'
        elif cor2 == 'verde':
            cor2 = '\033[0;32;40m'
        elif cor2 == 'amarelo':
            cor2 = '\033[0;33;40m'
        elif cor2 == 'azul':
            cor2 = '\033[0;34;40m'
        elif cor2 == 'ciano':
            cor2 = '\033[0;36;40m'
        else:
            cor2 = ''

        fim = '\033[m'

        if texto2 != '':
            texto3 = f'{cor}{texto}{fim} {cor2}{texto2}{fim}'
        
        else:
            texto3 = f'{cor}{texto}{fim}'

        for char in texto3:
            if vel == '':
                print(f'{char}', end="", flush=True)
                sleep(0.03)  # quanto menor o valor, mais rápido será escrito o texto
            
            else:
                print(f'{char}', end="", flush=True)
                sleep(float(vel))
        print()

    def dropar_item(self):

        RPG.limpar_tela()

        monstro_ativo = self.cursor.execute('''
        SELECT * FROM monstro_ativo
        ''').fetchone()[0]

        self.player_status()

        if self.player_xp > self.xp_necessario:
            self.cursor.execute('''
            UPDATE player SET xp = xp_necessario
            ''').fetchone()

        self.conn.commit()


        escolha_aleatoria = choice([0, 1, 1, 2])

        RPG.titulo('VITÓRIA')

        RPG.frase('Você derrotou o monstro!', 'verde')
        sleep(self.velocidade_texto)


        if monstro_ativo == 'goblin':
            
            RPG.frase(f'Você ganhou {self.xp_gerado_goblin} de EXP!')
            
            sleep(self.velocidade_texto)

        if monstro_ativo == 'goblin_xama':

            RPG.frase(f'Você ganhou {self.xp_gerado_goblin_xama} de EXP!')
            
            sleep(self.velocidade_texto)
        
        self.resetar_status()

        if escolha_aleatoria == 0:

            RPG.frase('\nNenhum item foi dropado', 'amarelo')
            sleep(self.velocidade_texto)

        else:

            RPG.frase('\nUm item foi dropado!', 'amarelo')
            sleep(self.velocidade_texto)
           
            #CALIBURN
            if escolha_aleatoria == 1: 
                RPG.limpar_tela()


                self.caliburn()

                sleep(self.velocidade_texto)
                print('(1) Pegar')
                
                sleep(self.velocidade_texto)
                print('(2) Descartar')                                                        
                    
                escolha = RPG.tecla_acao()

                if escolha == '1':
                    self.cursor.execute('''
                    INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                    SELECT nome, tipo, dano, beneficio, equipado
                    FROM itens WHERE id = 1
                ''')
                    self.conn.commit()

                    RPG.frase('\nItem adicionado ao inventário', 'verde')

                if escolha == '2':
                    RPG.frase('\nItem descartado', 'vermelho')


            #ELIXIR
            if escolha_aleatoria == 2:
                RPG.limpar_tela()


                self.elixir()

                sleep(self.velocidade_texto)
                print('(1) Pegar')

                sleep(self.velocidade_texto)
                print('(2) Descartar')                                                        
                    
                escolha = RPG.tecla_acao()

                if escolha == '1':
                    self.cursor.execute('''
                    INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                    SELECT nome, tipo, dano, beneficio, equipado
                    FROM itens WHERE id = 2
                ''')
                    self.conn.commit()

                    RPG.frase('\nItem adicionado ao inventário', 'verde')


                if escolha == '2':
                    RPG.frase('\nItem descartado', 'vermelho')

        self.player_status()

        if self.player_xp == self.xp_necessario:
            self.subir_de_nivel()

        else:
            self.monstro_ativo()

    def resetar_status(self):

        self.cursor.execute(f'''
        UPDATE monstro_ativo SET nome = 'vazio'
        ''')

        self.cursor.execute(f'''
        UPDATE player SET vida = vida_padrao
        ''')

        self.cursor.execute(f'''
        UPDATE goblin SET vida = vida_padrao
        ''')
        
        self.cursor.execute(f'''
        UPDATE goblin_xama SET vida = vida_padrao
        ''')

        self.conn.commit()

    def voce_morreu(self):
        self.resetar_status()
        RPG.limpar_tela()

        RPG.titulo('DERROTA', 'vermelho')

        RPG.frase('Você Morreu!', 'vermelho')
        
        sleep(self.velocidade_texto)

        RPG.frase('\nPressione ENTER para continuar')

        keyboard.wait('enter')
        self.mapa()

    def posicao_x(self):
        while True:
            item_procurado = 'X'


            for i, listas in enumerate(self.lista):
                try:
                
                    posicao = listas.index(item_procurado)
                    
                    return f'{i}'

            
                except ValueError:

                    continue
            break

    def mapa(self):

        self.lista = [
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],
        [' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' ']
        ]
        
        jogador_icon = ['X']
        self.ignorar_posicao_atual = 0


        ultima_posicao = self.cursor.execute('''
        SELECT ultima_posicao FROM player
        ''').fetchone()[0]

        self.lista.insert(ultima_posicao, jogador_icon)

        controle = 'W A S D'

        while True:
        
            RPG.limpar_tela()

            self.player_status()

            RPG.titulo('STATUS')


            print(self.player_ficha)

            spawnar_mob = randint(0, 8)
            posicao_mob = randint(0, 8)
            
            pos_x = int(self.posicao_x())


            segmento = 10
            for i in range(0, len(self.lista), segmento):
                print(''.join(map(str, self.lista[i:i + segmento])))
            

            print(f'''\n{controle}''')
            controle = ''
            

            self.cursor.execute(f'''
            UPDATE player SET ultima_posicao = {pos_x}
            ''').fetchone()
            self.conn.commit()

            if posicao_mob == spawnar_mob:
                 
            #função para ocasionalmente não iniciar o combate de
                if self.ignorar_posicao_atual == 0:
                    self.ignorar_posicao_atual = 1
                    pass
                
                else:
                    self.combate()
            

                

            wasd = RPG.tecla_mover()

    #///////////////////////////////////////////////////     
            
            if wasd == 'w' or wasd == 'up':
                #evita quando o jogador chegar no limite do mapa não pular para outro lugar
                
                if pos_x in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x, jogador_icon)
                
                

                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x - 10, jogador_icon)

    #///////////////////////////////////////////////////
            
            if wasd == 'a' or wasd == 'left':
                if pos_x in {
                    0, 10, 20, 30, 40, 50, 60, 70, 80,
                    90, 100, 110, 120, 130, 140, 150}:
                    
                    del self.lista[pos_x]
                    self.lista.insert(pos_x, jogador_icon)
                
                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x - 1, jogador_icon)

    #///////////////////////////////////////////////////
            
            if wasd == 's' or wasd == 'down':
                if pos_x in {150, 151, 152, 153, 154, 155, 156, 157, 158, 159}:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x, jogador_icon)
                
                

                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x + 10, jogador_icon)

    #///////////////////////////////////////////////////

            if wasd == 'd' or wasd == 'right' :
                if pos_x in {
                    9, 19, 29, 39, 49, 59, 69, 79, 89,
                    99, 109, 119, 129, 139, 149, 159}:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x, jogador_icon)
                

                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x + 1, jogador_icon)

    #///////////////////////////////////////////////////
            if wasd == 'i':
                self.inventario() 

    def limpar_tela():
        os.system('cls')

    def monstro_ativo(self):
        
        self.ignorar_posicao_atual = 0

        monstro = self.cursor.execute('''
        SELECT nome FROM monstro_ativo
        ''').fetchone()[0]
        
        if monstro == 'vazio':
            self.mapa()

        if monstro == 'goblin':
           self.goblin() 

        if monstro == 'goblin_xama':
            self.goblin_xama()

    def subir_de_nivel(self):
        RPG.limpar_tela()

        RPG.titulo('SUBIU DE NÍVEL!')
        
        #subindo quantidade de via total
        self.cursor.execute('''
        UPDATE player SET vida = (vida * taxa_vida)
        ''').fetchone()

        self.cursor.execute('''
        UPDATE player SET vida_padrao = vida
        ''').fetchone()

        #subindo taxa de dano
        self.cursor.execute('''
        UPDATE player SET dano_padrao = (dano_padrao + taxa_dano)
        ''').fetchone()

        self.cursor.execute('''
        UPDATE player SET dano = (dano + taxa_dano)
        ''').fetchone()

        #subindo de nível
        self.cursor.execute('''
        UPDATE player SET nivel = nivel + 1
        ''').fetchone()

        #subindo taxa necessaria de xp para próximo nível
        self.cursor.execute('''
        UPDATE player SET xp_necessario = (xp_necessario * taxa_proximo_nivel)
        ''').fetchone()

        #reduzindo xp obtido a zero após subir de nivel
        self.cursor.execute('''
        UPDATE player SET xp = 0
        ''').fetchone()

        self.conn.commit()


        nivel_atual = self.cursor.execute('''
        SELECT nivel FROM player
        ''').fetchone()[0]

        vida_atual = self.cursor.execute('''
        SELECT vida FROM player
        ''').fetchone()[0]

        dano_atual = self.cursor.execute('''
        SELECT dano_padrao FROM player
        ''').fetchone()[0]

        
        RPG.frase(f'Nível: {nivel_atual - 1:.0f} >', 'amarelo', f'{nivel_atual:.0f}', 'verde')
        RPG.frase(f'Vida: {vida_atual / 1.1:.0f} >', 'amarelo', f'{vida_atual:.0f}', 'verde')
        RPG.frase(f'Dano: {dano_atual - 1:.0f} >', 'amarelo', f'{dano_atual:.0f}', 'verde')

        sleep(self.velocidade_texto)


        RPG.frase('\nPressione ENTER para continuar')

        keyboard.wait('enter')

        self.monstro_ativo()

    def combate(self):

        if self.player_nivel < 4:

            self.cursor.execute(f'''
            UPDATE monstro_ativo SET nome = 'goblin'
            ''')
            self.conn.commit()

            self.goblin()

        else:

            monstro_escolhido = choice([1, 2])
            
            if monstro_escolhido == 1:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin'
                ''')
                self.conn.commit()

                self.goblin()
            

            if monstro_escolhido == 2:
                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin_xama'
                ''')
                self.conn.commit()

                self.goblin_xama()
        
    def goblin(self):

        while True:
            self.player_status()
            self.goblin_status()

            fugir = randint(1, 2)

            RPG.limpar_tela()
            
            acao_do_monstro = choice([
                self.goblin_dano_fraco,
                self.goblin_dano_medio,
                self.goblin_dano_forte
                ])

#///////////////////////////////////////////////////////////////////////////
           
            RPG.titulo('COMBATE')
                
            print(f'{self.goblin_ficha}\n\n')

            print(f'\n\n{self.player_ficha}')

            print('\n(1)Atacar')
            print('(2)Inventário')
            print('(3)Fugir\n')

            print('Escolha uma ação')
            acao = RPG.tecla_acao()

#//////////////////////////////////////////////////////////////////////////////
           
            if acao == '1':
                #///////////////////////////////////////////////////////////////

                #Vez do player

                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                print(f'{self.goblin_ficha}\n\n')
            
                print(f'\n\n{self.player_ficha}')
            
                
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE goblin SET vida = vida - {self.player_dano}
                ''')
                self.conn.commit()

                self.goblin_status()

                #///////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.player_dano:.0f} de dano!')
                

                sleep(self.velocidade_combate)
                
                #///////////////////////////////////////////////////////////////

                #morte do monstro
                if self.goblin_vida <= 0:   
                    
                    self.xp_gerado_goblin = randint(10, 20)

                    self.cursor.execute(f'''
                    UPDATE player SET xp = xp + {self.xp_gerado_goblin}
                    ''')

                    self.conn.commit()

                    self.dropar_item()


#/////////////////// Vez do monstro ////////////////////////////////////////////////
                RPG.limpar_tela()
                RPG.titulo('TURNO DO MONSTRO!')

                print(f'{self.goblin_ficha}\n\n')
            
                RPG.cor(f'\n\n{self.player_ficha}')
            
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE player SET vida = vida - {acao_do_monstro}''')
                self.conn.commit()
               
                #///////////////////////////////////////////////////////////////

                self.player_status()

                RPG.limpar_tela()

                RPG.titulo('TURNO DO MONSTRO!')
                
                print(f'{self.goblin_ficha}\n\n')
            
                RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')
                
                print(f'\n\nO monstro te causou {acao_do_monstro} de dano!')

                sleep(self.velocidade_combate)

                #///////////////////////////////////////////////////////////////


            if acao == '2':
                self.inventario()


            if acao == '3':

                if fugir == 2:

                    RPG.limpar_tela()

                    RPG.titulo('SEU TURNO!')

                    print(f'{self.goblin_ficha}')

                    RPG.cor('\n\nSucesso ao tentar fugir', 'verde')

                    print(f'\n\n{self.player_ficha}')
                    
                    sleep(self.velocidade_combate)
                    
                    self.cursor.execute(f'''
                    UPDATE monstro_ativo SET nome = 'vazio'
                    ''')
                    self.conn.commit()
                    
                    self.resetar_status()
                    self.monstro_ativo()

                else:

                    RPG.limpar_tela()

                    RPG.titulo('SEU TURNO!')

                    print(f'{self.goblin_ficha}')

                    RPG.cor('\n\nFalhou ao tentar fugir', 'vermelho')

                    print(f'\n\n{self.player_ficha}')
                    
                    sleep(self.velocidade_combate)

#/////////////////// Vez do monstro ////////////////////////////////////////////////
                   
                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.goblin_ficha}\n\n')
                

                    RPG.cor(f'\n\n{self.player_ficha}')
                
                    sleep(self.velocidade_combate)
                
                    self.cursor.execute(f'''
                    UPDATE player SET vida = vida - {self.goblin_dano_critico}
                    ''')
                    self.conn.commit()

                    #///////////////////////////////////////////////////////////////

                    self.player_status()

                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.goblin_ficha}\n\n')
                
                    RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')

                    print(f'\n\nO monstro te causou {self.goblin_dano_critico} de dano!')
                    
                    sleep(self.velocidade_combate)

                    #///////////////////////////////////////////////////////////////

            if self.player_vida <= 0:
                self.voce_morreu()

    def goblin_xama(self):
        
        while True:
            self.player_status()
            self.goblin_xama_status()

            fugir = randint(1, 2)

            RPG.limpar_tela()

            acao_do_monstro = choice(
            [self.goblin_xama_dano_fraco,
             self.goblin_xama_dano_medio,
             self.goblin_xama_cura,
            ])

#/////////////////////////////////////////////////////////////////////////////
            RPG.titulo('COMBATE')

            print(f'{self.goblin_xama_ficha}\n\n')

            print(f'\n\n{self.player_ficha}')

            print('\n(1)Atacar')
            print('(2)Inventário')
            print('(3)Fugir\n')
            
            print('Escolha uma ação')
            
            acao = RPG.tecla_acao()

#/////////////////////////////////////////////////////////////////////////////
            if acao == '1':

                #vez do player

                RPG.limpar_tela()
                RPG.titulo('SEU TURNO!')

                print(f'{self.goblin_xama_ficha}\n\n')

                print(f'\n\n{self.player_ficha}')

                sleep(self.velocidade_combate)

                self.cursor.execute(f'''
                UPDATE goblin_xama SET vida = vida - {self.player_dano}
                ''')

                self.conn.commit()

                self.goblin_xama_status()
#/////////////////////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_xama_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.player_dano:.0f} de dano!')
                
                sleep(self.velocidade_combate)
#/////////////////////////////////////////////////////////////////////////////

                #morte do monstro
                if self.goblin_xama_vida <= 0:   
                    self.xp_gerado_goblin_xama = randint(25, 40)

                    self.cursor.execute(f'''
                    UPDATE player SET xp = xp + {self.xp_gerado_goblin_xama}
                    ''')

                    self.conn.commit()
                    self.dropar_item()

#/////////////////////////////////////////////////////////////////////////////
                #vez do monstro

                RPG.limpar_tela()
                RPG.titulo('TURNO DO MONSTRO!')

                print(f'{self.goblin_xama_ficha}\n\n')
            
                RPG.cor(f'\n\n{self.player_ficha}')
            
                sleep(self.velocidade_combate)

                if acao_do_monstro == self.goblin_xama_cura:

                    if self.goblin_xama_vida == 120:
                        
                        acao_do_monstro = choice(
                        [self.goblin_xama_dano_fraco,
                        self.goblin_xama_dano_medio,
                        ])

                        self.cursor.execute(f'''
                        UPDATE player SET vida = vida - {acao_do_monstro}''')
                        self.conn.commit()

                        self.player_status()
#///////////////////////////////////////////////////////////////////////////////////////

                        RPG.limpar_tela()

                        RPG.titulo('TURNO DO MONSTRO!')
                        
                        print(f'{self.goblin_xama_ficha}\n\n')
                    
                        RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')
                        
                        print(f'\n\nO monstro te causou {acao_do_monstro} de dano!')

                        sleep(self.velocidade_combate)
#////////////////////////////////////////////////////////////////////////////////////////

                    elif self.goblin_xama_vida < 120:

                        self.cursor.execute(f'''
                        UPDATE goblin_xama SET vida = vida + {acao_do_monstro}''')
                        
                        self.goblin_xama_status()

                        if self.goblin_xama_vida > 120:
                            self.cursor.execute(f'''
                            UPDATE goblin_xama SET vida = 120''')
                        
                        self.conn.commit()

                        self.goblin_xama_status()
#//////////////////////////////////////////////////////////////////////////////////////////

                        RPG.limpar_tela()

                        RPG.titulo('TURNO DO MONSTRO!')
                        
                        RPG.cor(f'{self.goblin_xama_ficha}\n\n', 'verde')
                    
                        print(f'\n\n{self.player_ficha}')
                        
                        print(f'\n\nO monstro curou {acao_do_monstro} de vida!')

                        sleep(self.velocidade_combate)
#///////////////////////////////////////////////////////////////////////////////////////////

                else:
                    self.cursor.execute(f'''
                        UPDATE player SET vida = vida - {acao_do_monstro}''')
                    self.conn.commit()

                    self.player_status()

                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.goblin_xama_ficha}\n\n')
                
                    RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')
                    
                    print(f'\n\nO monstro te causou {acao_do_monstro} de dano!')

                    sleep(self.velocidade_combate)

            if acao == '2':
                    self.inventario()

            if acao == '3':

                    if fugir == 2:

                        RPG.limpar_tela()
                        RPG.titulo('SEU TURNO!')

                        print(f'{self.goblin_xama_ficha}')

                        RPG.cor('\n\nSucesso ao tentar fugir', 'verde')

                        print(f'\n\n{self.player_ficha}')
                        
                        sleep(self.velocidade_combate)
                        
                        self.cursor.execute(f'''
                        UPDATE monstro_ativo SET nome = 'vazio'
                        ''')
                        self.conn.commit()

                        self.resetar_status()
                        self.monstro_ativo()

                    else:

                        RPG.limpar_tela()

                        RPG.titulo('SEU TURNO!')

                        print(f'{self.goblin_xama_ficha}')

                        RPG.cor('\n\nFalhou ao tentar fugir', 'vermelho')

                        print(f'\n\n{self.player_ficha}')
                        
                        sleep(self.velocidade_combate)
        #//////////////////////////////////////////////////////////////////////////////////
                        #vez do monstro

                        RPG.limpar_tela()

                        RPG.titulo('TURNO DO MONSTRO!')
                        
                        print(f'{self.goblin_xama_ficha}\n\n')
                    

                        print(f'\n\n{self.player_ficha}')
                    
                        sleep(self.velocidade_combate)
                    
                        self.cursor.execute(f'''
                        UPDATE player SET vida = vida - {self.goblin_xama_dano_critico}
                        ''')
                        self.conn.commit()

                        self.player_status()
        #///////////////////////////////////////////////////////////////////////////////////
                        
                        RPG.limpar_tela()

                        RPG.titulo('TURNO DO MONSTRO!')
                        
                        print(f'{self.goblin_xama_ficha}\n\n')

                        RPG.cor(f'\n\n{self.player_ficha}','vermelho')
                    
                        print(f'\n\nO monstro te causou {self.goblin_xama_dano_critico} de dano!')

                        sleep(self.velocidade_combate)
                
            if self.player_vida <= 0:
                self.voce_morreu()

    def teclas_inventario():
         while True:       
            tempo_espera = 0.2

            acao = keyboard.read_key('')
   
            sleep(tempo_espera)
            return acao

    def tecla_acao():
        
        while True:       
            tempo_espera = 0.2

            acao = keyboard.read_key('')

            
            if acao == '1':
                sleep(tempo_espera)
                return '1'
            
            if acao == '2':
                sleep(tempo_espera)
                return '2'

            if acao == '3':
                sleep(tempo_espera)
                return '3'

            if acao == 'esc':
                sleep(tempo_espera)
                return 'esc'
            
    def tecla_mover():
        x_speed = 0.2
        
        while True:       

            wasd = keyboard.read_key('')

            
            if wasd == 'w':
                sleep(x_speed)
                return 'w'
            
            if wasd == 'a':
                sleep(x_speed)
                return 'a'
            
            if wasd == 's':
                sleep(x_speed)
                return 's'
    
            if wasd == 'd':
                sleep(x_speed)
                return 'd'

            if wasd == 'i':
                sleep(x_speed)
                return 'i'

            if wasd == 'up':
                sleep(x_speed)
                return 'up'
            
            if wasd == 'left':
                sleep(x_speed)
                return 'left'

            if wasd == 'down':
                sleep(x_speed)
                return 'down'
            
            if wasd == 'right':
                sleep(x_speed)
                return 'right'
            
    def cor(texto, cor=''):

        if cor == 'vermelho':
            cor = '\033[0;31;40m'
        
        if cor == 'verde':
            cor = '\033[0;32;40m'

        if cor == 'amarelo':
            cor = '\033[0;33;40m'
        
        if cor == 'azul':
            cor = '\033[0;34;40m'

        if cor == 'ciano':
            cor = '\033[0;36;40m'
        
        fim = '\033[m'

        print(f'{cor}{texto}{fim}')


def main():
    game = RPG()
    game.mapa()
    # game.goblin()    
    # game.goblin_xama()

if __name__ == '__main__':
    main()


