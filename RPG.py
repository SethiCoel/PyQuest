import os
from random import randint, choice
from time import sleep
import keyboard
import sqlite3



class RPG:
    def __init__(self):
        self.banco_dados()
        self.ficha_player()
        self.ficha_goblin()
        self.ficha_goblin_xama()
        self.velocidade_combate = 2
        self.velocidade_texto = 1

    def __str__(self):
        pass
    
    
    def banco_dados(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

#////////// criando a tabela do jogador //////////////////////////////
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
        nome TEXT,
        nivel INTEGER,
        vida INTEGER,
        dano INTEGER
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
        dano_critico INTEGER
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
        dano_critico INTEGER
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
            self.cursor.execute('''
            INSERT INTO player (nivel, vida, dano) 
            VALUES (1, 100, 10)                                           
        ''')
        
#////////// adicionando dados a tabela de itens //////////////////////////////
        if conferir_dados_itens is None:
            self.cursor.execute('''
            INSERT INTO itens (nome, tipo, dano, beneficio, equipado)
            VALUES
            ('Caliburn', 'Espada', 5, NULL, '[ ]'),
            ('Elixir', 'Poção de Cura', NULL, 20, '[ ]')      
        ''')
            
#/////////// adicionando dados a tabela goblin ////////////////////////////////
        if conferir_dados_goblin is None:
            self.cursor.execute('''
            INSERT INTO goblin (nome, vida, dano_fraco, dano_medio, dano_forte, dano_critico)
            VALUES ('Goblin', 15, 100, 10, 15, 20)
        ''')
            
#/////////// adicionando dados a tabela goblin xamã ////////////////////////////////
        if conferir_dados_goblin_xama is None:
            self.cursor.execute('''
            INSERT INTO goblin_xama (nome, vida, dano_fraco, dano_medio, cura, dano_critico)
            VALUES ('Goblin Xamã', 120, 10, 15, 5, 25)
    	''')

#////////// adicionando dados a tabela inventário do jogador //////////////////////////////     
        if conferir_dados_inventario is None:
            self.cursor.execute('''
                INSERT INTO inventario (nome, tipo, dano, beneficio, equipado)
                SELECT nome, tipo, dano, beneficio, equipado
                FROM itens WHERE id = 2
            ''') #ELIXIR

        self.conn.commit()

#//////////////////////////////////////////////////////////////////////////////
    def ficha_player(self):
        self.player_name = ''

        self.player_vida = self.cursor.execute('''
        SELECT vida FROM player ''').fetchone()[0]

        self.player_damage = self.cursor.execute('''
        SELECT dano FROM player ''').fetchone()[0]
        
        self.player_ficha = f'Player ----- {self.player_vida}HP'

#//////////////////////////////////////////////////////////////////////////////
    def ficha_goblin(self):
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

        self.goblin_ficha = f'{self.goblin_nome} ----- {self.goblin_vida}HP'

#//////////////////////////////////////////////////////////////////////////////
    def ficha_goblin_xama(self):
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

        self.goblin_xama_ficha = f'{self.goblin_xama_nome} ----- {self.goblin_xama_vida}HP'

#//////////////////////////////////////////////////////////////////////////////
    def inventario(self):
        RPG.limpar_tela()

        vel_item = 0.03

        jogador_vida = self.cursor.execute('''
        SELECT vida FROM player
        ''').fetchone()[0]

        self.itens = self.cursor.execute('''
        SELECT * FROM inventario
        ''').fetchall()

        posicao_itens = []
        item_ids = []

        tamanho_hud = 30

        nome_centralizado = 'Inventário'.center(tamanho_hud - 2)
        

        RPG.cor(f'╔{'═' * (tamanho_hud - 2)}╗', 'amarelo')
        RPG.cor(f'║{nome_centralizado}║', 'amarelo')
        RPG.cor(f'╠{'═' * (tamanho_hud - 2)}╣', 'amarelo')

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
            
            if self.item_especifico[1] == 'Caliburn':
                
                self.caliburn()

                print('(1) Equipar/Desequipar')
                print('(2) Descartar')
                
                print('\nESC Voltar')

                acao = RPG.tecla_acao()

                verificar_se_tem_algo_equipado = self.cursor.execute(f'''
                SELECT id FROM inventario WHERE equipado = '[*]' 
                ''').fetchone()


                if acao == '1':
                    self.ficha_player()

                    self.cursor.execute('''
                    SELECT * FROM inventario''')

                    if verificar_se_tem_algo_equipado is not None:

                        if item_ids[int(listar_itens)-1] != verificar_se_tem_algo_equipado[0]:

                            RPG.frase('\nUm outro item ja está equipado!', 'vermelho', vel_item)
                            sleep(self.velocidade_texto)
                            self.inventario()
                    
                    if verificar_se_tem_algo_equipado is None or verificar_se_tem_algo_equipado[0] == item_ids[int(listar_itens)-1]:

                        if self.player_damage >= 15:
                            
                            
                            self.cursor.execute(f'''
                            UPDATE player SET dano = 10''')

                            self.cursor.execute(f'''
                            UPDATE inventario SET equipado = '[ ]'
                            WHERE id = {item_ids[int(listar_itens)-1]} 
                            ''')

                            self.conn.commit()
                            
                            RPG.frase(f'\n{self.item_especifico[1]} desequipada!', 'amarelo', vel_item)
                            sleep(self.velocidade_texto)


                        if self.player_damage == 10:
                            
                            self.cursor.execute(f'''
                            UPDATE player SET dano = dano + {self.item_especifico[3]}''')
                            
                            self.cursor.execute(f'''
                            UPDATE inventario SET equipado = '[*]'
                            WHERE id = {item_ids[int(listar_itens)-1]}   
                            ''')
                            
                            self.conn.commit()

                            RPG.frase(f'\n{self.item_especifico[1]} equipada!', 'verde', vel_item)
                            sleep(self.velocidade_texto)
                
                if acao == '2':

                    if verificar_se_tem_algo_equipado[0] == item_ids[int(listar_itens)-1]:
                        self.cursor.execute(f'''
                        UPDATE player SET dano = 10''')
                    
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')

                    self.conn.commit()

                    RPG.frase('Caliburn descartada!', 'vermelho', vel_item)
                    sleep(self.velocidade_texto)

                if acao == 'esc':
                    self.inventario()

                self.inventario()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            if self.item_especifico[1] == 'Elixir':
                val_elixir = self.cursor.execute('''
                SELECT beneficio FROM itens WHERE id = 2
                ''').fetchone()[0] 
                self.elixir()

                print('(1) Usar')
                print('(2) Descartar')
                
                print('\nESC Voltar')

                acao = RPG.tecla_acao()

                if acao == '1':

                    if jogador_vida < 100:
                        self.cursor.execute(f'''
                        UPDATE player SET vida = (
                        vida + {val_elixir})
                        ''')                        
                        self.conn.commit()
                        RPG.frase('\nElixir usado!', 'verde', vel_item)
                        sleep(self.velocidade_texto)

                        self.cursor.execute(f'''
                        DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                        ''')
                        
                        self.conn.commit()
                        
                        jogador_vida = self.cursor.execute('''
                        SELECT vida FROM player
                        ''').fetchone()[0]

        

                        if jogador_vida > 100:
                                self.cursor.execute(f'''
                                UPDATE player SET vida = (100)
                                ''')
                                self.conn.commit()
                        
                    if jogador_vida == 100:
                        RPG.frase('\nSua vida está cheia!', 'vermelho', vel_item)
                        sleep(self.velocidade_texto)  

                    
                if acao == '2':
                    self.cursor.execute(f'''
                    DELETE FROM inventario WHERE id = {item_ids[int(listar_itens)-1]}
                    ''')
                    self.conn.commit()

                    RPG.frase('\nElixir descartado!', 'vermelho', vel_item)
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

    def frase(texto, cor='', vel=''):

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

        for char in texto + "\n":
            if vel == '':
                print(f'{cor}{char}{fim}', end="", flush=True)
                sleep(0.06) # quanto menor o valor, mais rápido será escrito o texto

            else:
                print(f'{cor}{char}{fim}', end="", flush=True)
                sleep(vel)

    def dropar_item(self):
        self.resetar_status()

        RPG.limpar_tela()
       
        
        escolha_aleatoria = choice([0, 1, 1, 2])

        RPG.titulo('VITÓRIA')

        RPG.frase('Você derrotou o monstro!', 'verde')
        sleep(self.velocidade_texto)
       
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


        sleep(self.velocidade_texto)
        self.mapa()

    def resetar_status(self):

        self.cursor.execute(f'''
        UPDATE player SET vida = 100
        ''')

        self.cursor.execute(f'''
        UPDATE goblin SET vida = 100
        ''')
        
        self.cursor.execute(f'''
        UPDATE goblin_xama SET vida = 120
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
        [' '],[' '],[' '],
        [' '],['X'],[' '],
        [' '],[' '],[' ']
        ]
        
        ignore_first4 = 0


        controle = 'W A S D'

        while True:
            
            RPG.limpar_tela()

            spawnar_mob = randint(0, 8)
            
            
            
            pos_x = int(self.posicao_x())


            print(f'''                     
{self.lista[0]}{self.lista[1]}{self.lista[2]}
{self.lista[3]}{self.lista[4]}{self.lista[5]}
{self.lista[6]}{self.lista[7]}{self.lista[8]}
    ''')
            

            print(f'''{controle}''')
            controle = ''
            

            if pos_x == spawnar_mob:

            #função para ocasionalmente não iniciar o combate assim que abrir o jogo
                if spawnar_mob == 4:
                    if ignore_first4 == 0:
                        ignore_first4 = 1
                        pass
                    
                    else:
                        self.combate()
                
                else:
                    self.combate()


            wasd = RPG.tecla_mover()

            

    #///////////////////////////////////////////////////     
            
            if wasd == 'w':
                
                if pos_x == 0:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                elif pos_x == 1:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                elif pos_x == 2:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x - 3,['X'])

    #///////////////////////////////////////////////////
            
            if wasd == 'a':
                if pos_x == 0:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                elif pos_x == 3:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                elif pos_x == 6:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x - 1, ['X'])

    #///////////////////////////////////////////////////
            
            if wasd == 's':
                if pos_x == 6:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                elif pos_x == 7:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                elif pos_x == 8:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])

                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x + 3,['X'])

    #///////////////////////////////////////////////////

            if wasd == 'd':
                if pos_x == 2:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                elif pos_x == 5:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                elif pos_x == 8:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x,['X'])
                
                else:
                    del self.lista[pos_x]
                    self.lista.insert(pos_x + 1, ['X'])

    #///////////////////////////////////////////////////
            if wasd == 'i':
                self.inventario() 

    def limpar_tela():
        os.system('cls')

    def monstro_ativo(self):
        
        monstro = self.cursor.execute('''
        SELECT nome FROM monstro_ativo
        ''').fetchone()[0]
        
        if monstro == 'vazio':
            self.mapa()

        if monstro == 'goblin':
           self.goblin() 

        if monstro == 'goblin_xama':
            self.goblin_xama()

    def combate(self):

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
            self.ficha_player()
            self.ficha_goblin()

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
                UPDATE goblin SET vida = vida - {self.player_damage}
                ''')
                self.conn.commit()

                self.ficha_goblin()

                #///////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.player_damage} de dano!')
                

                sleep(self.velocidade_combate)
                
                #///////////////////////////////////////////////////////////////

                #morte do monstro
                if self.goblin_vida <= 0:   
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

                self.ficha_player()

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
                    self.mapa()

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

                    self.ficha_player()

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
            self.ficha_player()
            self.ficha_goblin_xama()

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
                UPDATE goblin_xama SET vida = vida - {self.player_damage}
                ''')

                self.conn.commit()

                self.ficha_goblin_xama()
#/////////////////////////////////////////////////////////////////////////////
                
                RPG.limpar_tela()

                RPG.titulo('SEU TURNO!')

                RPG.cor(f'{self.goblin_xama_ficha}\n\n', 'vermelho')
            
                print(f'\n\n{self.player_ficha}')
                
                print(f'\n\nVocê causou {self.player_damage} de dano!')
                
                sleep(self.velocidade_combate)
#/////////////////////////////////////////////////////////////////////////////

                #morte do monstro
                if self.goblin_xama_vida <= 0:   
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

                        self.ficha_player()
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
                        
                        self.ficha_goblin_xama()

                        if self.goblin_xama_vida > 120:
                            self.cursor.execute(f'''
                            UPDATE goblin_xama SET vida = 120''')
                        
                        self.conn.commit()

                        self.ficha_goblin_xama()
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

                    self.ficha_player()

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
                        self.mapa()

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

                        self.ficha_player()
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


