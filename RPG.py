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
        
        #mapa 1
        self.icon_porta = '|'
        self.ico_item = '▪'
        self.ico_vazio = ' '

        coo_chave_spawn_mapa_1 = 54
        coo_porta_spawn_mapa_1 = 97
        coo_porta_chefe_mapa_1 = 365
        coo_item_1_mapa_1 = 150
        coo_item_2_mapa_1 = 376


        # jogador
        player_nome = 'Player'
        self.player_nivel = 1
        self.player_vida = 20
        self.player_dano = 2
        self.player_xp = 0
        self.player_vida_padrao = self.player_vida
        self.player_dano_padrao = self.player_dano
        self.posicao_inicial = 86
        self.maximo_itens = 9


        #UP do jogador
        taxa_aumento_vida = 1.1
        taxa_aumento_dano = 1
        taxa_proximo_nivel = 1.4
        self.xp_necessario = 20


        # goblin
        goblin_nome = 'Goblin'
        goblin_vida = 16
        goblin_dano_fraco = 2
        goblin_dano_medio = 3
        goblin_dano_forte = 4
        goblin_dano_critico = 5


        # goblin Xamã
        goblin_xama_nome = 'Goblin Xamã'
        goblin_xama_vida = 32
        goblin_xama_dano_fraco = 4
        goblin_xama_dano_medio = 6
        goblin_xama_cura = 10
        goblin_xama_dano_critico = 7

        # esqueleto
        esqueleto_nome = 'Esqueleto'
        esqueleto_vida = 10
        esqueleto_dano = 3

        # orc
        orc_nome = 'Orc'
        orc_vida = 40
        orc_dano_fraco = 7
        orc_dano_medio = 8
        orc_dano_forte = 10
        orc_dano_critico = 11


#///////// criando tabela de icones /////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS icones (
        ico_porta TEXT,
        ico_item TEXT, 
        ico_vazio TEXT
        )
    ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS icones_mapa1 (
        ico_porta1 TEXT,
        ico_porta2 TEXT,
        ico_item1 TEXT,
        ico_item2 TEXT,
        ico_item3 TEXT, 
        ico_vazio TEXT
        )
    ''')

#///////// criando tabelas de mapas /////////////////////////////

        #mapa 1
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS mapa_1 (
        coo_porta_spawn INTEGER,
        coo_porta_boss INTEGER,
        coo_chave_spawn INTEGER,
        coo_item_1 INTEGER,
        coo_item_2 INTEGER                  
        )
    ''')

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

#///////// criando a tabela do esqueleto //////////////////////////////
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS esqueleto (
                nome TEXT,
                vida INTEGER,
                dano INTEGER,
                vida_padrao INTEGER
                )
            ''')

#///////// criando a tabela do orc ////////////////////////////////////
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS orc (
                nome TEXT,
                vida INTEGER,
                dano_fraco INTEGER,
                dano_medio INTEGER,
                dano_forte INTEGER,
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

#///////// criando tabela de missão mapa1 ////////////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS missao_mapa1(
        orelha INTEGER,
        qtd_orelha INTEGER, 
        olho INTEGER, 
        qtd_olho INTEGER, 
        cranio INTEGER, 
        qtd_cranio INTEGER,
        dente INTEGER,
        qtd_dente
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
        
        conferir_dados_esqueleto = self.cursor.execute('''
        SELECT * FROM esqueleto
    ''').fetchone()
        
        conferir_dados_orc = self.cursor.execute('''
        SELECT * FROM orc
        ''').fetchone()

        conferir_dados_icones = self.cursor.execute('''
        SELECT * FROM icones
    ''').fetchone()

        conferir_dados_icones_mapa1 = self.cursor.execute('''
        SELECT * FROM icones_mapa1
    ''').fetchone()

        conferir_dados_mapa_1 = self.cursor.execute('''
        SELECT * FROM mapa_1 
    ''').fetchone()

        conferir_dados_missao_mapa1 = self.cursor.execute('''
        SELECT * FROM missao_mapa1
    ''').fetchone()

#////////// adicionando dados a tabela do jogador //////////////////////////////
        if conferir_dados_player is None:
            self.cursor.execute(f'''
            INSERT INTO player (nome, nivel, vida, dano, xp, vida_padrao, dano_padrao,
            taxa_vida, taxa_dano, taxa_proximo_nivel, xp_necessario, ultima_posicao) 
            VALUES (
            '{player_nome}', {self.player_nivel}, {self.player_vida}, 
            {self.player_dano}, {self.player_xp}, {self.player_vida_padrao}, 
            {self.player_dano_padrao}, {taxa_aumento_vida}, {taxa_aumento_dano},
            {taxa_proximo_nivel}, {self.xp_necessario}, {self.posicao_inicial}
            )                                           
        ''')
        
#////////// adicionando dados a tabela de itens //////////////////////////////
        if conferir_dados_itens is None:
            self.cursor.execute('''
            INSERT INTO itens (nome, tipo, dano, beneficio, equipado)
            VALUES
            ('Caliburn', 'Espada', 2, NULL, '[ ]'),
            ('Elixir', 'Poção de Cura', NULL, 20, '[ ]'),
            ('Chave de Ferro', 'Chave Velha', NULL, NULL, '[ ]'),
            ('Poção Pequena', 'Poção de Cura', NULL, 8, '[ ]'),
            ('Ragnarok', 'Espada', 5, NULL, '[ ]'),
            ('Orelha de Goblin', 'Detritos de Monstro', NULL, NULL, '[ ]'),
            ('Olho de Goblin Xamã', 'Detritos de Monstro', NULL, NULL, '[ ]'),
            ('Crânio de Esqueleto', 'Detritos de Monstro', NULL, NULL, '[ ]'),
            ('Dente de Orc', 'Detritod de Monstro', NULL, NULL, '[ ]')      
        ''')
            
#/////////// adicionando dados a tabela goblin ////////////////////////////////
        if conferir_dados_goblin is None:
            self.cursor.execute(f'''
            INSERT INTO goblin (nome, vida, dano_fraco, dano_medio, dano_forte, dano_critico, vida_padrao)
            VALUES ('{goblin_nome}', {goblin_vida}, {goblin_dano_fraco},
            {goblin_dano_medio}, {goblin_dano_forte}, {goblin_dano_critico}, {goblin_vida})
        ''')
            
#/////////// adicionando dados a tabela goblin xamã /////////////////////////////////////
        if conferir_dados_goblin_xama is None:
            self.cursor.execute(f'''
            INSERT INTO goblin_xama (nome, vida, dano_fraco, dano_medio, cura, dano_critico, vida_padrao)
            VALUES ('{goblin_xama_nome}', {goblin_xama_vida}, {goblin_xama_dano_fraco},
            {goblin_xama_dano_medio}, {goblin_xama_cura}, {goblin_xama_dano_critico}, {goblin_xama_vida})
    	''')

#/////////// adicionando dados a tabela esqueleto /////////////////////////////////////////
        if conferir_dados_esqueleto is None:
            self.cursor.execute(f'''
        INSERT INTO esqueleto (nome, vida, dano, vida_padrao)
        VALUES ('{esqueleto_nome}', {esqueleto_vida}, {esqueleto_dano}, {esqueleto_vida})    
        ''')

#////////// adicionando dados a tabela orc ///////////////////////////////////////////////
        if conferir_dados_orc is None:
            self.cursor.execute(f'''
            INSERT INTO orc (nome, vida, dano_fraco, dano_medio, dano_forte, dano_critico, vida_padrao)
            VALUES ('{orc_nome}', {orc_vida}, {orc_dano_fraco}, {orc_dano_medio},
            {orc_dano_forte}, {orc_dano_critico}, {orc_vida})
            ''')

#///////// adcionando dados a tabela icones ////////////////////////////////////////////////
        if conferir_dados_icones is None:
            self.cursor.execute(f'''
            INSERT INTO ICONES (
            ico_porta, ico_item, ico_vazio) VALUES (
            '{self.icon_porta}', '{self.ico_item}', '{self.ico_vazio}')
            ''')

        if conferir_dados_icones_mapa1 is None:
            self.cursor.execute(f'''
            INSERT INTO icones_mapa1 (
            ico_porta1, ico_porta2, ico_item1,
            ico_item2, ico_item3, ico_vazio)
            VALUES (
            '{self.icon_porta}', '{self.icon_porta}', '{self.ico_item}',
            '{self.ico_item}', '{self.ico_item}', '{self.ico_vazio}'
            )
        ''')

#////////// adicionando dados a tabela mapa 1 //////////////////////////////////////////////    
        if conferir_dados_mapa_1 is None:
            self.cursor.execute(f'''
            INSERT INTO mapa_1 (
            coo_porta_spawn, coo_porta_boss, coo_chave_spawn,
            coo_item_1, coo_item_2)
            VALUES (
            {coo_porta_spawn_mapa_1}, {coo_porta_chefe_mapa_1}, {coo_chave_spawn_mapa_1},
            {coo_item_1_mapa_1},{coo_item_2_mapa_1})
            ''')
       
#////////// adicionando dados a tabela missão mapa 1
        if conferir_dados_missao_mapa1 is None:
            self.cursor.execute('''
            INSERT INTO missao_mapa1 (
            orelha, qtd_orelha, olho, qtd_olho, cranio, qtd_cranio, dente, qtd_dente)
            VALUES(1, 0, 1, 0, 1, 0, 1, 0)
        ''')


        self.conn.commit()

#//////////////////////////////////////////////////////////////////////////////
    def player_status(self):
        self.player_nome = self.cursor.execute('''
        SELECT nome FROM player ''').fetchone()[0]

        self.jogador_nivel = self.cursor.execute('''
        SELECT nivel FROM player ''').fetchone()[0]

        self.jogador_vida = self.cursor.execute('''
        SELECT vida FROM player ''').fetchone()[0]

        self.jogador_dano = self.cursor.execute('''
        SELECT dano FROM player ''').fetchone()[0]
        
        self.jogador_xp = self.cursor.execute('''
        SELECT xp FROM player ''').fetchone()[0]

        self.vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM player ''').fetchone()[0]

        self.jogador_xp_necessario = self.cursor.execute('''
        SELECT xp_necessario FROM player ''').fetchone()[0]

        inventario = self.cursor.execute('SELECT * FROM inventario').fetchall()
    

        self.quantidade_itens = len(inventario)

        self.player_ficha = f'''{self.player_nome}: {'█' * int(self.jogador_vida)} {'-' * int(self.vida_padrao - self.jogador_vida)}| {self.jogador_vida:.0f}/{self.vida_padrao:.0f} 
Dano: {self.jogador_dano:.0f} {' ' * int(self.vida_padrao)}   Nível: {self.jogador_nivel}
EXP: {self.jogador_xp:.0f}/{self.jogador_xp_necessario:.0f} {' ' * int(self.vida_padrao)} Inv: {len(inventario)}/{self.maximo_itens}
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

        self.goblin_ficha = f'{self.goblin_nome}: {'█' * int(self.goblin_vida)} {'-' * int(self.goblin_vida_padrao - self.goblin_vida)}| {self.goblin_vida:.0f}/{self.goblin_vida_padrao}'

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


        self.goblin_xama_ficha = f'{self.goblin_xama_nome}: {'█' * int(self.goblin_xama_vida)} {'-' * int(self.goblin_xama_vida_padrao - self.goblin_xama_vida)}| {self.goblin_xama_vida:.0f}/{self.goblin_xama_vida_padrao}'

#/////////////////////////////////////////////////////////////////////////////
    def esqueleto_status(self):
        self.esqueleto_nome = self.cursor.execute('''
        SELECT nome FROM esqueleto ''').fetchone()[0]

        self.esqueleto_vida = self.cursor.execute('''
        SELECT vida FROM esqueleto ''').fetchone()[0]

        self.esqueleto_dano = self.cursor.execute('''
        SELECT dano FROM esqueleto ''').fetchone()[0]

        self.esqueleto_dano_critico = self.cursor.execute('''
        SELECT dano FROM esqueleto''').fetchone()[0]

        self.esqueleto_vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM esqueleto ''').fetchone()[0]

        self.esqueleto_ficha = f'{self.esqueleto_nome}: {'█' * int(self.esqueleto_vida)} {'-' * int(self.esqueleto_vida_padrao - self.esqueleto_vida)}| {self.esqueleto_vida:.0f}/{self.esqueleto_vida_padrao}'

#//////////////////////////////////////////////////////////////////////////////
    def orc_status(self):
        self.orc_nome = self.cursor.execute('''
        SELECT nome FROM orc ''').fetchone()[0]

        self.orc_vida = self.cursor.execute('''
        SELECT vida FROM orc ''').fetchone()[0]

        self.orc_dano_fraco = self.cursor.execute('''
        SELECT dano_fraco FROM orc ''').fetchone()[0]

        self.orc_dano_medio = self.cursor.execute('''
        SELECT dano_medio FROM orc ''').fetchone()[0]

        self.orc_dano_forte = self.cursor.execute('''
        SELECT dano_forte FROM orc ''').fetchone()[0]

        self.orc_dano_critico = self.cursor.execute('''
        SELECT dano_critico FROM orc''').fetchone()[0]

        self.orc_vida_padrao = self.cursor.execute('''
        SELECT vida_padrao FROM orc ''').fetchone()[0]

        self.orc_ficha = f'{self.orc_nome}: {'█' * int(self.orc_vida)} {'-' * int(self.orc_vida_padrao - self.orc_vida)}| {self.orc_vida:.0f}/{self.orc_vida_padrao}'

#//////////////////////////////////////////////////////////////////////////////
    def inventario(self):
        RPG.limpar_tela()
        
        self.player_status()

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

        tamanho_hud = 40

        RPG.titulo('Inventário')

        RPG.cor(f'{self.player_ficha}\n')
        hud_cima = tamanho_hud - 5
        hud_meio = tamanho_hud - 36
        hud_baixo = hud_cima

        RPG.cor(f'╔{'═' * (hud_cima)}╗', 'amarelo')
       

        for num, item in enumerate(self.itens):
            indice = num + 1
            if indice < 10:

                indice_formatado = f'({indice}) '
            else:
                indice_formatado = f'({indice})'

            item_ids.append(item[0])

            posicao_itens.append(str(indice))

            RPG.cor(f'''║{indice_formatado} {item[1].ljust(tamanho_hud - 15)} {item[5].ljust(hud_meio)}║''', 'amarelo')

        RPG.cor(f'╚{'═' * (hud_baixo)}╝', 'amarelo')
        
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

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Chave de Ferro':
                self.chave_de_ferro()

                RPG.cor('ESC voltar')

                acao = RPG.tecla_acao()

                if acao	== 'esc':
                    self.inventario()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Poção Pequena':
                cura_pocao_pequena = self.cursor.execute('''
                SELECT beneficio FROM itens WHERE id = 4
                ''').fetchone()[0] 
                
                
                self.pocao_pequena()

                print('(1) Usar')
                print('(2) Descartar')
                
                print('\nESC Voltar')

                acao = RPG.tecla_acao()

                if acao == '1':

                    if jogador_vida < jogador_vida_padrao:
                        self.cursor.execute(f'''
                        UPDATE player SET vida = vida + {cura_pocao_pequena}
                        ''')                        
                        self.conn.commit()
                        RPG.frase('\nPoção Pequena usada!', 'verde')
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

                    RPG.frase('\nPoção Pequena descartada!', 'vermelho')
                    sleep(self.velocidade_texto)

                if acao == 'esc':
                    self.inventario()
                
                self.inventario()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Ragnarok':

                verificar_se_tem_algo_equipado = self.cursor.execute(f'''
                SELECT id FROM inventario WHERE equipado = '[*]' 
                ''').fetchone()

                self.ragnarok()

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
                        UPDATE player SET dano = dano + {self.item_especifico[3]}''')
                        
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

                    RPG.frase('Ragnarok descartada!', 'vermelho')
                    sleep(self.velocidade_texto)

                if acao == 'esc':
                    self.inventario()

                self.inventario()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Orelha de Goblin':
                self.orelha_goblin()

                RPG.cor('(1) Descartar')
                RPG.cor('ESC voltar')

                acao = RPG.tecla_acao()

                if acao == '1':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')

                    self.conn.commit()

                    RPG.frase('\nOrelha de Goblin descartada!', 'vermelho')
                    sleep(self.velocidade_texto)

                    self.inventario()

                if acao	== 'esc':
                    self.inventario()
           
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Olho de Goblin Xamã':
                self.olho_goblin_xama()

                RPG.cor('(1) Descartar')
                RPG.cor('ESC voltar')

                acao = RPG.tecla_acao()

                if acao == '1':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')
                    self.conn.commit()

                    RPG.frase('\nOlho de Goblin Xamã descartado!', 'vermelho')
                    sleep(self.velocidade_texto)

                    self.inventario()

                if acao	== 'esc':
                    self.inventario()
            
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Crânio de Esqueleto':
                self.cranio_esqueleto()

                RPG.cor('(1) Descartar')
                RPG.cor('ESC voltar')

                acao = RPG.tecla_acao()

                if acao == '1':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')
                    self.conn.commit()

                    RPG.frase('\nCrânio de Esqueleto descartado!', 'vermelho')

                    sleep(self.velocidade_texto)

                    self.inventario()

                if acao	== 'esc':
                    self.inventario()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Dente de Orc':
                self.dente_orc()

                RPG.cor('(1) Descartar')
                RPG.cor('ESC voltar')

                acao = RPG.tecla_acao()

                if acao == '1':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')
                    self.conn.commit()

                    RPG.frase('\nDente de Orc descartado!', 'vermelho')
                    
                    sleep(self.velocidade_texto)

                    self.inventario()

                if acao	== 'esc':
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

#//////////////////////////////////////////////////////////////////////////////
    def chave_de_ferro(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[2]

        nome = item_especifico[1]
        tipo = item_especifico[2]


        RPG.hud_item(nome, tipo)

#//////////////////////////////////////////////////////////////////////////////
    def pocao_pequena(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[3]

        nome = item_especifico[1]
        tipo = item_especifico[2]
        cura = item_especifico[4]
        
        RPG.hud_item(nome, tipo, f'{cura} de cura')

#/////////////////////////////////////////////////////////////////////////////
    def ragnarok(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[4]

        nome = item_especifico[1]
        tipo = item_especifico[2]
        dano = item_especifico[3]
        
        RPG.hud_item(nome, tipo, f'{dano} de dano')

#//////////////////////////////////////////////////////////////////////////////
    def orelha_goblin(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[5]

        nome = item_especifico[1]
        tipo = item_especifico[2]


        RPG.hud_item(nome, tipo)

#//////////////////////////////////////////////////////////////////////////////
    def olho_goblin_xama(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[6]

        nome = item_especifico[1]
        tipo = item_especifico[2]


        RPG.hud_item(nome, tipo)

#/////////////////////////////////////////////////////////////////////////////
    def cranio_esqueleto(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[7]

        nome = item_especifico[1]
        tipo = item_especifico[2]


        RPG.hud_item(nome, tipo)

#/////////////////////////////////////////////////////////////////////////////
    def dente_orc(self):
        RPG.limpar_tela()

        itens = self.cursor.execute('''
        SELECT * FROM itens
        ''').fetchall()

        item_especifico = itens[8]

        nome = item_especifico[1]
        tipo = item_especifico[2]


        RPG.hud_item(nome, tipo)

    def hud_item(nome='', tipo='', efeito=''):
        
        tamanho_hud = 30
        
        nome_centralizado = nome.center(tamanho_hud - 2)
        
        tipo_formatado = f"Tipo: {tipo}".ljust(tamanho_hud - 3)
        
        if efeito == '':
            efeito_formatado = ''.ljust(tamanho_hud - 3)
        
        else:
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

        if self.jogador_xp > self.jogador_xp_necessario:
            self.cursor.execute('''
            UPDATE player SET xp = xp_necessario
            ''').fetchone()

        self.conn.commit()


        escolha_aleatoria = choice([0, 1, 2, 2, 2, 2])

        monstro_drop = choice([ 0, 1, 1])

        RPG.titulo('VITÓRIA')

        RPG.frase('Você derrotou o monstro!', 'verde')
        sleep(self.velocidade_texto)


#/////////////////////////////////////////////////////////////////////////////
        if monstro_ativo == 'goblin':
            self.player_status()
            
            item_goblin = self.cursor.execute('''
            SELECT nome FROM itens WHERE id = 6 
            ''').fetchone()[0]

            RPG.frase(f'Você ganhou {self.xp_gerado_goblin} de EXP!')
            
            if monstro_drop == 1:

                if self.quantidade_itens >= self.maximo_itens:
               
                    RPG.frase('\nIventário Cheio!', 'vermelho')
                
                else:
                    self.cursor.execute('''
                        INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                        SELECT nome, tipo, dano, beneficio, equipado
                        FROM itens WHERE id = 6
                    ''')
                    self.conn.commit()

                    RPG.frase(f'\n{item_goblin} adicionado ao inventário', 'verde')

            sleep(self.velocidade_texto)

#//////////////////////////////////////////////////////////////////////////////////
        elif monstro_ativo == 'goblin_xama':
            self.player_status()

            item_goblin_xama = self.cursor.execute('''
            SELECT nome FROM itens WHERE id = 7 
            ''').fetchone()[0]

            RPG.frase(f'Você ganhou {self.xp_gerado_goblin_xama} de EXP!')
               
            if self.quantidade_itens < self.maximo_itens:
                
                #ELIXIR
                self.cursor.execute('''
                INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                SELECT nome, tipo, dano, beneficio, equipado
                FROM itens WHERE id = 2
                ''')    

                self.conn.commit()

                RPG.frase('\nElixir adicionado ao inventário', 'verde')    


                #DETRITO DO MONSTRO
                if monstro_drop == 1:
                    self.player_status()

                    if self.quantidade_itens < self.maximo_itens:

                        self.cursor.execute('''
                        INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                        SELECT nome, tipo, dano, beneficio, equipado
                        FROM itens WHERE id = 7
                        ''')

                        self.conn.commit()

                        RPG.frase(f'\n{item_goblin_xama} adicionado ao inventário', 'verde')

                    elif self.quantidade_itens >= self.maximo_itens:
                        RPG.frase('\nInventário Cheio!', 'vermelho')

            sleep(self.velocidade_texto)

#//////////////////////////////////////////////////////////////////////////////////////
        elif monstro_ativo == 'esqueleto':
            
            self.player_status()

            item_esqueleto = self.cursor.execute('''
            SELECT nome FROM itens WHERE id = 8 
            ''').fetchone()[0]

            RPG.frase(f'Você ganhou {self.xp_gerado_esqueleto} de EXP!')
        

            if monstro_drop == 1:
                if self.quantidade_itens >= self.maximo_itens:
               
                    RPG.frase('Iventário Cheio!', 'vermelho')

                else:
                    self.cursor.execute('''
                        INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                        SELECT nome, tipo, dano, beneficio, equipado
                        FROM itens WHERE id = 8
                    ''')
                    self.conn.commit()

                    RPG.frase(f'\n{item_esqueleto} adicionado ao inventário', 'verde')

            sleep(self.velocidade_texto)
        
#///////////////////////////////////////////////////////////////////////////////////////        
        elif monstro_ativo == 'orc':
            
            self.player_status()

            item_orc = self.cursor.execute('''
            SELECT nome FROM itens WHERE id = 9 
            ''').fetchone()[0]

            RPG.frase(f'Você ganhou {self.xp_gerado_orc} de EXP!')
        
            if monstro_drop == 1:
                if self.quantidade_itens >= self.maximo_itens:
               
                    RPG.frase('Iventário Cheio!', 'vermelho')
                
                else:
                    self.cursor.execute('''
                        INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                        SELECT nome, tipo, dano, beneficio, equipado
                        FROM itens WHERE id = 9
                    ''')
                    self.conn.commit()

                    RPG.frase(f'\n{item_orc} adicionado ao inventário', 'verde')

            sleep(self.velocidade_texto)

#/////////////////////////////////////////////////////////////////////////////////////////
        
        RPG.cor('\nPressione qualquer tecla para continuar', 'azul')
        keyboard.read_key('')

        self.player_status()
        self.resetar_status()

        if escolha_aleatoria == 0:

            RPG.frase('\nNenhum item foi dropado', 'amarelo')
            sleep(self.velocidade_texto)

        else:

            if self.quantidade_itens >= self.maximo_itens:
               
               if monstro_drop == 0:
                    RPG.frase('\nIventário Cheio!', 'vermelho')
            
            elif self.quantidade_itens < self.maximo_itens:
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


                #POÇÃO PEQUENA
                if escolha_aleatoria == 2:
                    RPG.limpar_tela()


                    self.pocao_pequena()

                    sleep(self.velocidade_texto)
                    print('(1) Pegar')

                    sleep(self.velocidade_texto)
                    print('(2) Descartar')                                                        
                        
                    escolha = RPG.tecla_acao()

                    if escolha == '1':
                        self.cursor.execute('''
                        INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                        SELECT nome, tipo, dano, beneficio, equipado
                        FROM itens WHERE id = 4
                    ''')
                        self.conn.commit()

                        RPG.frase('\nItem adicionado ao inventário', 'verde')


                    if escolha == '2':
                        RPG.frase('\nItem descartado', 'vermelho')

            self.player_status()

            sleep(self.velocidade_texto)

        if self.jogador_xp == self.jogador_xp_necessario:
            self.subir_de_nivel()

        else:
            self.monstro_ativo()

    def resetar_status(self):

        self.cursor.execute(f'''
        UPDATE monstro_ativo SET nome = 'vazio'
        ''')

        self.cursor.execute(f'''
        UPDATE goblin SET vida = vida_padrao
        ''')
        
        self.cursor.execute(f'''
        UPDATE goblin_xama SET vida = vida_padrao
        ''')

        self.cursor.execute(f'''
        UPDATE esqueleto SET vida = vida_padrao
        ''')

        self.cursor.execute(f'''
        UPDATE orc SET vida = vida_padrao
        ''')

        self.conn.commit()

    def voce_morreu(self):

        RPG.limpar_tela()

        RPG.titulo('DERROTA', 'vermelho')

        RPG.frase('Você Morreu!', 'vermelho')
        
        sleep(self.velocidade_texto)

        
        #resetar nivel
        self.cursor.execute(f'''
        UPDATE player SET nivel = {self.player_nivel}
        ''')

        #resetar vida
        self.cursor.execute(f'''
        UPDATE player SET vida = {self.player_vida}
        ''')
        self.cursor.execute(f'''
        UPDATE player SET vida_padrao = {self.player_vida}
        ''')

        #resetar dano
        self.cursor.execute(f'''
        UPDATE player SET dano = {self.player_dano}
        ''')
        self.cursor.execute(f'''
        UPDATE player SET dano_padrao = {self.player_dano}
        ''')

        #resetar XP
        self.cursor.execute(f'''
        UPDATE player SET xp = {self.player_xp}
        ''')

        #resetar XP necessario
        self.cursor.execute(f'''
        UPDATE player SET xp_necessario = {self.xp_necessario}
        ''')

        #resetar posição
        self.cursor.execute(f'''
            UPDATE player SET ultima_posicao = {self.posicao_inicial}
            ''')
        
        #apagar itens do inventário
        self.cursor.execute(f'''
        DELETE FROM inventario ''')

        #resetando o mapa
        self.cursor.execute(f'''
            UPDATE icones_mapa1 SET
            ico_porta1 = '{self.icon_porta}',
            ico_porta2 = '{self.icon_porta}',
            ico_item1 = '{self.ico_item}',
            ico_item2 = '{self.ico_item}',
            ico_item3 = '{self.ico_item}'
        ''')

        #resetar item missão:
        self.cursor.execute('''
        UPDATE missao_mapa1 SET
        qtd_orelha = 0,
        qtd_olho = 0,
        qtd_cranio = 0,
        qtd_dente = 0    
        ''')

        self.conn.commit()
        
        self.resetar_status()

        RPG.frase('\nPressione qualquer tecla para continuar')

        keyboard.read_key('')
        self.mapa()

    def posicao_x(self):
        while True:

            for i, listas in enumerate(self.mapa_lista):
                try:
                
                    posicao = listas.index(self.jogador_icon)
            
                    return i

                    
                except Exception as error:

                    continue
            break
    
    def interacao_mapa(self):
        
#/////// coordenada de cada item ///////////////////////        
        self.coo_porta_spawn = self.cursor.execute('''
        SELECT coo_porta_spawn FROM mapa_1 
        ''').fetchone()[0]

        coo_chave_spawn = self.cursor.execute('''
        SELECT coo_chave_spawn FROM mapa_1
        ''').fetchone()[0]

        self.coo_porta_chefe = self.cursor.execute('''
        SELECT coo_porta_boss FROM mapa_1 
        ''').fetchone()[0]

        coo_item_2 = self.cursor.execute('''
        SELECT coo_item_1 FROM mapa_1 
        ''').fetchone()[0]

        coo_item_3 = self.cursor.execute('''
        SELECT coo_item_2 FROM mapa_1 
        ''').fetchone()[0]


#////// icone de cada item ///////////////////////////////////

        self.ico_porta1 = self.cursor.execute('''
        SELECT ico_porta1 FROM icones_mapa1                                
        ''').fetchone()[0]

        self.ico_porta2 = self.cursor.execute('''
        SELECT ico_porta2 FROM icones_mapa1                                
        ''').fetchone()[0]

        ico_item1 = self.cursor.execute('''
        SELECT ico_item1 FROM icones_mapa1                               
        ''').fetchone()[0]

        ico_item2 = self.cursor.execute('''
        SELECT ico_item2 FROM icones_mapa1                               
        ''').fetchone()[0]

        ico_item3 = self.cursor.execute('''
        SELECT ico_item3 FROM icones_mapa1                               
        ''').fetchone()[0]

        self.ico_vazio = self.cursor.execute('''
        SELECT ico_vazio FROM icones_mapa1
        ''').fetchone()[0]

        #insere porta no spawn
        self.mapa_lista[self.coo_porta_spawn] = self.ico_porta1
    
        #insere icone de item no mapa
        self.mapa_lista[coo_chave_spawn] = ico_item1

        #insere porta na area do boss
        self.mapa_lista[self.coo_porta_chefe] = self.ico_porta2

        #insere icone de item no mapa
        self.mapa_lista[coo_item_2] = ico_item2
        self.mapa_lista[coo_item_3] = ico_item3
#///////////////////////////////////////////////////////////////////////////

        ultima_posicao = self.cursor.execute('''
        SELECT ultima_posicao FROM player
        ''').fetchone()[0]
        

        chave_ferro = self.cursor.execute('''
        SELECT nome FROM inventario WHERE nome = 'Chave de Ferro'
        ''').fetchone()
        

        #adicionar chave no inventario
        if ultima_posicao == coo_chave_spawn:
            
            if ico_item1 == self.ico_vazio:
                pass
            
            else:
                self.cursor.execute('''
                UPDATE icones_mapa1 SET ico_item1 = ico_vazio''')

                #CHAVE
                self.cursor.execute('''
                    INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                    SELECT nome, tipo, dano, beneficio, equipado
                    FROM itens WHERE id = 3
                ''')
                RPG.cor('Você achou uma chave!', 'verde')
        
        #abrir portas
        if chave_ferro is not None:
            
            if ultima_posicao == self.coo_porta_spawn - 1:
                self.cursor.execute('''
                    UPDATE icones_mapa1 SET ico_porta1 = ico_vazio''')
                
                self.cursor.execute(f'''
                    DELETE FROM inventario WHERE nome = 'Chave de Ferro'
                    ''')
                
                RPG.cor('Porta Destrancada!', 'verde')

        #tentar abrir a porta sem a chave
        elif ultima_posicao == self.coo_porta_spawn - 1:
            if self.ico_porta1 != self.ico_vazio:
                RPG.cor('Porta Trancada!', 'vermelho')

        #tentar abrir a porta do chefe sem a chave
        elif ultima_posicao == self.coo_porta_chefe - 1:
            if self.ico_porta2 != self.ico_vazio:
                RPG.cor('Porta Trancada!', 'vermelho')

        #adicionar elixir item no inventario
        if ultima_posicao == coo_item_2:
            if ico_item2 == self.ico_vazio:
                pass
            
            else:
              self.cursor.execute('''
                UPDATE icones_mapa1 SET ico_item2 = ico_vazio''')  
                
                #ELIXIR
              self.cursor.execute('''
                INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                SELECT nome, tipo, dano, beneficio, equipado
                FROM itens WHERE id = 2
                ''')
              RPG.cor('Você achou um Elixir!', 'verde')

        #adicionar ragnarok ao inventario
        if ultima_posicao == coo_item_3:

            if ico_item3 == self.ico_vazio:
                pass
            
            else:
              self.cursor.execute('''
                UPDATE icones_mapa1 SET ico_item3 = ico_vazio''')  
                
                #ELIXIR
              self.cursor.execute('''
                INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                SELECT nome, tipo, dano, beneficio, equipado
                FROM itens WHERE id = 5
                ''')
              RPG.cor('Ragnarok adicionado ao inventário!', 'verde')

        self.conn.commit()
        
    def dialogo_mapa1(self):

        ultima_posicao = self.cursor.execute('''
        SELECT ultima_posicao FROM player
        ''').fetchone()[0]


        orelha = self.cursor.execute('''
        SELECT orelha FROM missao_mapa1 ''').fetchone()[0]
        
        qtd_orelha = self.cursor.execute('''
        SELECT qtd_orelha FROM missao_mapa1 ''').fetchone()[0]

        item_orelha = self.cursor.execute('''
        SELECT nome FROM inventario WHERE nome = 'Orelha de Goblin'
        ''').fetchone()


        olho = self.cursor.execute('''
        SELECT olho FROM missao_mapa1 ''').fetchone()[0]

        qtd_olho = self.cursor.execute('''
        SELECT qtd_olho FROM missao_mapa1 ''').fetchone()[0]
        
        item_olho = self.cursor.execute('''
        SELECT nome FROM inventario WHERE nome = 'Olho de Goblin Xamã'
        ''').fetchone()


        cranio = self.cursor.execute('''
        SELECT cranio FROM missao_mapa1 ''').fetchone()[0]

        qtd_cranio = self.cursor.execute('''
        SELECT qtd_cranio FROM missao_mapa1 ''').fetchone()[0]

        item_cranio = self.cursor.execute('''
        SELECT nome FROM inventario WHERE nome = 'Crânio de Esqueleto'
        ''').fetchone()


        dente = self.cursor.execute('''
        SELECT dente FROM missao_mapa1 ''').fetchone()[0]

        qtd_dente = self.cursor.execute('''
        SELECT qtd_dente FROM missao_mapa1 ''').fetchone()[0]

        item_dente = self.cursor.execute('''
        SELECT nome FROM inventario WHERE nome = 'Dente de Orc'
        ''').fetchone()
        

        if ultima_posicao == 318:
            
            if item_orelha is not None:
                
                if qtd_orelha > orelha:
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_orelha = orelha
                    ''')

                elif qtd_orelha < orelha:    
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_orelha = (qtd_orelha + 1)
                    ''')

                    self.cursor.execute('''
                    DELETE FROM inventario WHERE nome = 'Orelha de Goblin'
                    ''')

                    RPG.frase('Entregou Orelha de Goblin', 'vermelho')
                    sleep(self.velocidade_texto)
            
            if item_olho is not None:

                if qtd_olho > olho:
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_olho = olho
                    ''')

                elif qtd_olho < olho:    
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_olho = (qtd_olho + 1)
                    ''')

                    self.cursor.execute('''
                    DELETE FROM inventario WHERE nome = 'Olho de Goblin Xamã'
                    ''')

                    RPG.frase('Entregou Olho de Goblin Xamã', 'vermelho')
                    sleep(self.velocidade_texto)

            if item_cranio is not None:
                
                if qtd_cranio > cranio:
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_cranio = cranio
                    ''')

                elif qtd_cranio < cranio:    
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_cranio = (qtd_cranio + 1)
                    ''')

                    self.cursor.execute('''
                    DELETE FROM inventario WHERE nome = 'Crânio de Esqueleto'
                    ''')

                    RPG.frase('Entregou Crânio de Esqueleto', 'vermelho')
                    sleep(self.velocidade_texto)

            if item_dente is not None:
                
                if qtd_dente > dente:
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_dente = dente
                    ''')

                elif qtd_dente < dente:    
                    self.cursor.execute('''
                    UPDATE missao_mapa1 SET qtd_dente = (qtd_dente + 1)
                    ''')

                    self.cursor.execute('''
                    DELETE FROM inventario WHERE nome = 'Dente de Orc'
                    ''')

                    RPG.frase('Entregou Dente de Orc', 'vermelho')
                    sleep(self.velocidade_texto)

            

            RPG.frase('Quero que você me traga algumas coisas...')
            sleep(self.velocidade_texto)

            qtd_orelha_att = self.cursor.execute('''
            SELECT qtd_orelha FROM missao_mapa1 ''').fetchone()[0]

            RPG.cor(f'\nx{orelha - qtd_orelha_att} Orelhas de Goblin')
            sleep(self.velocidade_texto)

            qtd_olho_att = self.cursor.execute('''
            SELECT qtd_olho FROM missao_mapa1 ''').fetchone()[0]

            RPG.cor(f'x{olho - qtd_olho_att} Olhos de Goblin Xamã')
            sleep(self.velocidade_texto)

            qtd_cranio_att = self.cursor.execute('''
            SELECT qtd_cranio FROM missao_mapa1 ''').fetchone()[0]

            RPG.cor(f'x{cranio - qtd_cranio_att} Crânio de Esqueleto')
            sleep(self.velocidade_texto)

            qtd_dente_att = self.cursor.execute('''
            SELECT qtd_dente FROM missao_mapa1 ''').fetchone()[0]

            RPG.cor(f'x{dente - qtd_dente_att} Dentes de Orc')
            sleep(self.velocidade_texto)

        if ultima_posicao == 402:

            RPG.frase('Vai precisar ficar bem forte para conseguir esses itens')
            
            RPG.frase('\nEncontrará esses monstros nos seguintes níveis:')
            sleep(self.velocidade_texto)

            RPG.cor('\nEsqueleto ----- NVL 1 ')
            sleep(self.velocidade_texto)

            RPG.cor('Goblin ----- NVL 2')
            sleep(self.velocidade_texto)

            RPG.cor('Goblin Xamã ----- NVL 4')
            sleep(self.velocidade_texto)

            RPG.cor('Orc ----- NVL 7')
            sleep(self.velocidade_texto)

        if qtd_orelha == orelha and qtd_olho == olho and qtd_cranio == cranio and qtd_dente == dente:
            
            if self.ico_porta2 == self.ico_vazio:
                pass
            
            else:
                self.cursor.execute('''
                UPDATE icones_mapa1 SET ico_porta2 = ico_vazio''')
            
                RPG.cor('Porta Destrancada!', 'verde')

        self.conn.commit()

    def mapa(self):
        
        mapa_string = f'''
╔═══════════╦═══════════════════════╦═══╗
║           ║                           ║
║                                   ║   ║
║           ║                       ║   ║
╠═══════════╩═══════════════════════╝  ═╣
║                                       ║
║            ═══════════════╦═══════════╣
║                           ║           ║
║                                       ║
║                           ║           ║
╚═══════════════════════════╩═══════════╝'''

        self.jogador_icon = '♙'
        self.guarda_icon = '♗'
        

        self.ignorar_posicao_atual = 0
        
        posicao_guarda_um = 320
        posicao_guarda_dois = 404

        self.ultima_posicao = self.cursor.execute('''
        SELECT ultima_posicao FROM player
        ''').fetchone()[0]
        
        self.mapa_lista = list(mapa_string)

        self.interacao_mapa()

        self.mapa_lista[self.ultima_posicao] = self.jogador_icon

        self.mapa_lista[posicao_guarda_um] = self.guarda_icon
        self.mapa_lista[posicao_guarda_dois] = self.guarda_icon

        controle = '''W A S D
i = inventário'''


        while True:
            
            RPG.limpar_tela()

            self.player_status()

       
            RPG.titulo('STATUS')

            print(self.player_ficha)

            
            spawnar_mob = randint(0, 8)
            posicao_mob = randint(0, 8)
            
            pos_x = self.posicao_x()

            mapa = ''.join(self.mapa_lista)
            
            
            self.mapa_lista = list(mapa_string)
            
            print(f'{' ' * 18}MAPA', end='')
           
            print(mapa)
            print(f'{controle}')
            controle = ''
            
            self.cursor.execute(f'''
            UPDATE player SET ultima_posicao = {pos_x}
            ''').fetchone()

            self.conn.commit()

            
            self.mapa_lista[posicao_guarda_um] = self.guarda_icon
            self.mapa_lista[posicao_guarda_dois] = self.guarda_icon
            
            self.interacao_mapa()
            self.dialogo_mapa1()
            
            if posicao_mob == spawnar_mob:

                if pos_x in {
                  44, 46, 48, 50, 52, 54, 86, 88,
                  90, 92, 94, 96, 128, 138, 132, 
                  134, 136, 138, 324, 326, 328, 
                  330, 332, 334, 318, 366, 368,
                  370, 372, 374, 376, 402, 408,
                  410, 412, 414, 416, 418,
                  148,108, 152, 150}: 
                   pass
               
                else:

                    #função para ocasionalmente não iniciar o combate de
                    if self.ignorar_posicao_atual == 0:
                        self.ignorar_posicao_atual = 1
                        pass
                    
                    else:
                        self.combate()
                

            wasd = RPG.tecla_mover()
            self.interacao_mapa()
    #///////////////////////////////////////////////////     
            
            if wasd == 'w' or wasd == 'up':
                
                #evita quando o jogador chegar no limite do mapa não pular para outro lugar
                
                if 44 <= pos_x <= 82 or 212 <= pos_x <= 246:
                    
                    self.mapa_lista[pos_x] = self.jogador_icon
                
                elif pos_x in {
                    250, 362}:
                    
                    self.mapa_lista[pos_x] = self.jogador_icon

                elif 308 <= pos_x <= 334:

                    self.mapa_lista[pos_x] = self.jogador_icon
                

                else:

                    self.mapa_lista[pos_x - 42] = self.jogador_icon
                

    #///////////////////////////////////////////////////
            
            if wasd == 'a' or wasd == 'left':
                if pos_x in {
                    44, 56, 86, 122, 128, 140,
                    164, 170, 182, 206, 212, 254, 296,
                    322, 324, 338, 380, 408, 406
                    }:
                    self.mapa_lista[pos_x] = self.jogador_icon
                
                else:
                    self.mapa_lista[pos_x - 2] = self.jogador_icon
                

    #///////////////////////////////////////////////////
            
            if wasd == 's' or wasd == 'down':
                if 380 <= pos_x <= 418 or 128 <= pos_x <= 162:

                    self.mapa_lista[pos_x] = self.jogador_icon

                elif pos_x in {
                    166, 362}:
    
                    self.mapa_lista[pos_x] = self.jogador_icon


                elif 224 <= pos_x <= 250:

                    self.mapa_lista[pos_x] = self.jogador_icon

                else:
                    self.mapa_lista[pos_x + 42] = self.jogador_icon

    #///////////////////////////////////////////////////

            if wasd == 'd' or wasd == 'right' :
                if pos_x in {
                    54, 82, 120, 124, 138, 162, 166,
                    206, 208, 250, 264, 292, 318, 322, 334,
                    376, 402, 406, 418
                    }:

                    self.mapa_lista[pos_x] = self.jogador_icon

                elif pos_x == self.coo_porta_spawn - 1:
            
                    if self.ico_porta1 == self.ico_vazio:
                        self.mapa_lista[pos_x + 2] = self.jogador_icon
                   
                    else:
                        self.mapa_lista[pos_x] = self.jogador_icon
                        self.interacao_mapa()
                
                elif pos_x == self.coo_porta_chefe - 1:

                    if self.ico_porta2 == self.ico_vazio:
                        self.mapa_lista[pos_x + 2] = self.jogador_icon

                    else:
                        self.mapa_lista[pos_x] = self.jogador_icon
                        self.interacao_mapa()

                else:
                    self.mapa_lista[pos_x + 2] = self.jogador_icon
                

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

        if monstro == 'esqueleto':
            self.esqueleto()

        if monstro == 'orc':
            self.orc()

    def subir_de_nivel(self):
        RPG.limpar_tela()

        RPG.titulo('SUBIU DE NÍVEL!')
        
        #subindo quantidade de via total
        self.cursor.execute('''
        UPDATE player SET vida_padrao = (vida_padrao * taxa_vida)
        ''').fetchone()

        self.cursor.execute('''
        UPDATE player SET vida = vida_padrao
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
        SELECT vida_padrao FROM player
        ''').fetchone()[0]

        dano_atual = self.cursor.execute('''
        SELECT dano_padrao FROM player
        ''').fetchone()[0]

        
        RPG.frase(f'Nível: {nivel_atual - 1:.0f} >', 'amarelo', f'{nivel_atual:.0f}', 'verde')
        RPG.frase(f'Vida: {vida_atual / 1.1:.0f} >', 'amarelo', f'{vida_atual:.0f}', 'verde')
        RPG.frase(f'Dano: {dano_atual - 1:.0f} >', 'amarelo', f'{dano_atual:.0f}', 'verde')

        sleep(self.velocidade_texto)


        RPG.frase('\nPressione qualquer tecla para continuar')

        keyboard.read_key('')

        self.monstro_ativo()

    def combate(self):

        if self.jogador_nivel == 1:

            self.cursor.execute(f'''
            UPDATE monstro_ativo SET nome = 'esqueleto'
            ''')
            self.conn.commit()

            self.esqueleto()

        if 2 <= self.jogador_nivel <= 3:

            monstro_escolhido = choice([1, 2, 2, 2])
            
            if monstro_escolhido == 1:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin'
                ''')
                self.conn.commit()

                self.goblin()
            
            if monstro_escolhido == 2:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'esqueleto'
                ''')
                self.conn.commit()

                self.esqueleto()

        if 4 <= self.jogador_nivel <= 6: 
            monstro_escolhido = choice([1, 2, 3, 3, 3])
            
            if monstro_escolhido == 1:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin'
                ''')
                self.conn.commit()

                self.goblin()
            
            if monstro_escolhido == 2:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'esqueleto'
                ''')
                self.conn.commit()

                self.esqueleto()

            if monstro_escolhido == 3:
                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin_xama'
                ''')
                self.conn.commit()

                self.goblin_xama()
        
        if self.jogador_nivel >= 7: 
            monstro_escolhido = choice([1, 2, 3, 4, 4, 4])
            
            if monstro_escolhido == 1:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin'
                ''')
                self.conn.commit()

                self.goblin()
            
            if monstro_escolhido == 2:

                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'esqueleto'
                ''')
                self.conn.commit()

                self.esqueleto()

            if monstro_escolhido == 3:
                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'goblin_xama'
                ''')
                self.conn.commit()

                self.goblin_xama()

            if monstro_escolhido == 4:
                self.cursor.execute(f'''
                UPDATE monstro_ativo SET nome = 'orc'
                ''')
                self.conn.commit()

                self.orc()
        
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
                UPDATE goblin SET vida = vida - {self.jogador_dano}
                ''')
                self.conn.commit()

                self.goblin_status()

                #///////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.jogador_dano:.0f} de dano!')
                

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

            if self.jogador_vida <= 0:
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
                UPDATE goblin_xama SET vida = vida - {self.jogador_dano}
                ''')

                self.conn.commit()

                self.goblin_xama_status()
#/////////////////////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_xama_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.jogador_dano:.0f} de dano!')
                
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

                    if self.goblin_xama_vida == self.goblin_xama_vida_padrao:
                        
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

                    elif self.goblin_xama_vida < self.goblin_xama_vida_padrao:

                        self.cursor.execute(f'''
                        UPDATE goblin_xama SET vida = vida + {acao_do_monstro}''')
                        
                        self.goblin_xama_status()

                        if self.goblin_xama_vida > self.goblin_xama_vida_padrao:
                            self.cursor.execute(f'''
                            UPDATE goblin_xama SET vida = vida_padrao''')
                        
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
                
            if self.jogador_vida <= 0:
                self.voce_morreu()

    def esqueleto(self):

        while True:
            self.player_status()
            self.esqueleto_status()

            fugir = randint(1, 2)

            RPG.limpar_tela()
            
            acao_do_monstro = self.esqueleto_dano

#///////////////////////////////////////////////////////////////////////////
           
            RPG.titulo('COMBATE')
                
            print(f'{self.esqueleto_ficha}\n\n')

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

                print(f'{self.esqueleto_ficha}\n\n')
            
                print(f'\n\n{self.player_ficha}')
            
                
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE esqueleto SET vida = vida - {self.jogador_dano}
                ''')
                self.conn.commit()

                self.esqueleto_status()

                #///////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.esqueleto_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.jogador_dano:.0f} de dano!')
                

                sleep(self.velocidade_combate)
                
                #///////////////////////////////////////////////////////////////

                #morte do monstro
                if self.esqueleto_vida <= 0:   
                    
                    self.xp_gerado_esqueleto = randint(10, 15)

                    self.cursor.execute(f'''
                    UPDATE player SET xp = xp + {self.xp_gerado_esqueleto}
                    ''')

                    self.conn.commit()

                    self.dropar_item()


#/////////////////// Vez do monstro ////////////////////////////////////////////////
                RPG.limpar_tela()
                RPG.titulo('TURNO DO MONSTRO!')

                print(f'{self.esqueleto_ficha}\n\n')
            
                RPG.cor(f'\n\n{self.player_ficha}')
            
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE player SET vida = vida - {acao_do_monstro}''')
                self.conn.commit()
               
                #///////////////////////////////////////////////////////////////

                self.player_status()

                RPG.limpar_tela()

                RPG.titulo('TURNO DO MONSTRO!')
                
                print(f'{self.esqueleto_ficha}\n\n')
            
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

                    print(f'{self.esqueleto_ficha}')

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

                    print(f'{self.esqueleto_ficha}')

                    RPG.cor('\n\nFalhou ao tentar fugir', 'vermelho')

                    print(f'\n\n{self.player_ficha}')
                    
                    sleep(self.velocidade_combate)

#/////////////////// Vez do monstro ////////////////////////////////////////////////
                   
                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.esqueleto_ficha}\n\n')
                

                    RPG.cor(f'\n\n{self.player_ficha}')
                
                    sleep(self.velocidade_combate)
                
                    self.cursor.execute(f'''
                    UPDATE player SET vida = vida - {self.esqueleto_dano_critico}
                    ''')
                    self.conn.commit()

                    #///////////////////////////////////////////////////////////////

                    self.player_status()

                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.esqueleto_ficha}\n\n')
                
                    RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')

                    print(f'\n\nO monstro te causou {self.esqueleto_dano_critico} de dano!')
                    
                    sleep(self.velocidade_combate)

                    #///////////////////////////////////////////////////////////////

            if self.jogador_vida <= 0:
                self.voce_morreu()        

    def orc(self):

        while True:
            self.player_status()
            self.orc_status()

            fugir = randint(1, 2)

            RPG.limpar_tela()
            
            acao_do_monstro = choice([
                self.orc_dano_fraco,
                self.orc_dano_medio,
                self.orc_dano_forte
                ])

#///////////////////////////////////////////////////////////////////////////
           
            RPG.titulo('COMBATE')
                
            print(f'{self.orc_ficha}\n\n')

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

                print(f'{self.orc_ficha}\n\n')
            
                print(f'\n\n{self.player_ficha}')
            
                
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE orc SET vida = vida - {self.jogador_dano}
                ''')
                self.conn.commit()

                self.orc_status()

                #///////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.orc_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.jogador_dano:.0f} de dano!')
                

                sleep(self.velocidade_combate)
                
                #///////////////////////////////////////////////////////////////

                #morte do monstro
                if self.orc_vida <= 0:   
                    
                    self.xp_gerado_orc = randint(60, 85)

                    self.cursor.execute(f'''
                    UPDATE player SET xp = xp + {self.xp_gerado_orc}
                    ''')

                    self.conn.commit()

                    self.dropar_item()


#/////////////////// Vez do monstro ////////////////////////////////////////////////
                RPG.limpar_tela()
                RPG.titulo('TURNO DO MONSTRO!')

                print(f'{self.orc_ficha}\n\n')
            
                RPG.cor(f'\n\n{self.player_ficha}')
            
                sleep(self.velocidade_combate)
            
                self.cursor.execute(f'''
                UPDATE player SET vida = vida - {acao_do_monstro}''')
                self.conn.commit()
               
                #///////////////////////////////////////////////////////////////

                self.player_status()

                RPG.limpar_tela()

                RPG.titulo('TURNO DO MONSTRO!')
                
                print(f'{self.orc_ficha}\n\n')
            
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

                    print(f'{self.orc_ficha}')

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

                    print(f'{self.orc_ficha}')

                    RPG.cor('\n\nFalhou ao tentar fugir', 'vermelho')

                    print(f'\n\n{self.player_ficha}')
                    
                    sleep(self.velocidade_combate)

#/////////////////// Vez do monstro ////////////////////////////////////////////////
                   
                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.orc_ficha}\n\n')
                

                    RPG.cor(f'\n\n{self.player_ficha}')
                
                    sleep(self.velocidade_combate)
                
                    self.cursor.execute(f'''
                    UPDATE player SET vida = vida - {self.orc_dano_critico}
                    ''')
                    self.conn.commit()

                    #///////////////////////////////////////////////////////////////

                    self.player_status()

                    RPG.limpar_tela()

                    RPG.titulo('TURNO DO MONSTRO!')
                    
                    print(f'{self.orc_ficha}\n\n')
                
                    RPG.cor(f'\n\n{self.player_ficha}', 'vermelho')

                    print(f'\n\nO monstro te causou {self.orc_dano_critico} de dano!')
                    
                    sleep(self.velocidade_combate)

                    #///////////////////////////////////////////////////////////////

            if self.jogador_vida <= 0:
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
    

if __name__ == '__main__':
    main()


