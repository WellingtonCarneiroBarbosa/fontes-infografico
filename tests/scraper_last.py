#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Instagram Scraper Comments
# Developed by Wellington Barbosa
# At May, 07 - 2020 
# Follow me on github https://github.com/wellingtoncarneirobarbosa
# --------------------------------------------------------------------
from pandas import ExcelWriter
from datetime import datetime
from slugify import slugify
import time, sys, platform, os, random, math, requests, re, json, hashlib, os
import keyboard
import string
from threading import *
import pandas as pd  
# -----
# api 
# -----
from api.instagram import Instagram

class instagramScraper:
    def __init__(self, sleep_between_requests=0):
        executionOn = platform.system()
        print("\n")
        print("\r[!] Executando o bot em sistema " + str(executionOn) )
        print("\r[!] Iniciado em => " + str(datetime.now().strftime("%d/%m/%Y")) + " as " + str(datetime.now().strftime("%H:%M")) )
        print("\n------------------------------------------------------\n" )
        print("\r[!] IMPORTANTE! LEIA ANTES DE EXECUTAR O BOT!\n \n" )
        print("\r[!] Recomendamos o uso de uma conta fake para a extracao dos comentarios.\n[!] Nao nos responsabilizamos caso sua conta seja permanentemente banida." )
        print("\r[!] Note que nao salvamos nenhum dos seus dados na web. Todos os dados e comentarios sao salvos em seu computador local." )
        print("\r \n \n[!] Ao fazer login pelo script, sua conta sera desconectada de todas as plataformas em que ela estiver conectada" )
        print("\r \n \n[!] NAO LOGUE NOVAMENTE ENQUANTO O BOT ESTIVER LIGADO" )
        print("\r[!] Isso causara uma falha no bot e sua conta podera ser banida" )
        print("\n------------------------------------------------------\n" )
        print("\n")
        self.start = datetime.now()

    def getLen(numero):
        numero = abs(int(numero))
        if numero < 2:
            return 1
        count = 0
        valor = 1
        while valor <= numero:
            valor *= 10
            count += 1
        return count

    # ---------------------
    # get user login
    # ---------------------
    def getLogin(self):
        # ------------------
        # login credencials
        # ------------------
        self.login = str(input("Insira seu username do instagram: "))
        self.password = str(input("Insira sua senha do instagram: "))

        # -------------------
        # show feedback
        # -------------------
        print( "\n------------------------------------------------------\n" )
        print( "\r[!] Tentando realizar login...."                          )
        print( "\n------------------------------------------------------\n" )
    

    def getPost(self):
        # ------------------
        # post credencials
        # ------------------
        while True:
            try:
                print( "\n------------------------------------------------------\n" )
                self.postCode = str(input("\r[!] Insira o ID da publicacao => "))
            except:
                print(  "\n------------------------------------------------------\n" )
                print(  "\r[!] Ops...\nEsse id e invalido" )
                print(  "\n------------------------------------------------------\n" )
                continue
            break
        print( "\n------------------------------------------------------\n" )
        self.qtdComments = int(input("\r[!] Insira a quantidade de comentarios que deseja extrair: "))
        print( "\n------------------------------------------------------\n" )
       
    def excel_exporter(names, comments, codes, self):
        try:
            m = 0
            fname = "comments.csv"
            while os.path.exists(fname):
                m += 1
                fname = "comments" + "(" + str(m) + ")" + ".csv"
            temp = {}                    
            temp_names = []
            temp_comments = []
            temp_codes = []
            temp_names.extend(names)
            temp_comments.extend(comments)
            temp_codes.extend(codes)
            temp.update({'a - username': temp_names, 'b - comment': temp_comments, 'c - codes': temp_codes})
            df = pd.DataFrame(temp)
            df.to_csv(fname, index=False, encoding='utf-8')
        except Exception as e:
            print("\rErro no codigo do excel_exporter")
            print("\rComunique o desenvolvedor")
            print("\rCodigo do erro (mostre isso ao desenvolvedor) => ")
            print(e)
    # ------------------
    # start scrapper
    # -----------------
    def scraper(self):
        # get api
        instagram = Instagram()

        while True:
            # ----------------
            # start try login
            # ----------------
            try:
                instagramScraper.getLogin(self)
                instagram.with_credentials(self.login, self.password)
                instagram.login()

            except Exception as e:
                print(    "\n------------------------------------------------------\n" )
                
                if(str(e) == "User credentials are wrong., Code:401"):
                    
                    print(    "\r[x] Login e/ou senha incorreto(s)" )
                    print(    "\n------------------------------------------------------\n" )
                    
                    continue
                break
                print(    "\r[x] Voce logou muitas vezes. O instagram bloqueou temporariamente o acesso do script a sua conta" )
                print(    "\rTente novamente daqui 10/30 minutos ou use outra conta para login" )
                print(    "\n------------------------------------------------------\n" )
                continue
            break
            # -----------------
            # end try login
            # ----------------

        # ---------------
        # logged in!
        # ---------------
        print("\n------------------------------------------------------\n" )
        print("\r[+] Login realizado com sucesso"                          )
        print("\n------------------------------------------------------\n" )
        # ---------------
        # try get post
        # ---------------
        try:
            instagramScraper.getPost(self)
            startExtractCommentsTime = datetime.now()
            print("\n------------------------------------------------------\n"             )
            print("\r[!] Carregando comentarios... isso pode levar horas"      )
            print("\r[!] Nao use o computador enquanto a extracao estiver sendo realizada." )
            print("\n------------------------------------------------------\n"             )
            comments = instagram.get_media_comments_by_id(self.postCode, self.qtdComments)
        except Exception as e:
            print("Um erro ocorreu :( reporte-o ao desenvolvedor \n \n")
            print(e)
            pass

        # -----------------
        # extract comments
        # -----------------
        users = []
        comments_getted = []
        i = 0
        l = 0

        endExtractCommentsTime = datetime.now()
        print("\n------------------------------------------------------\n"             )
        print("\r[+] Todos os comentarios foram obtidos com sucesso"                   )
        print("\r[!] Iniciando extracao dos dados obtidos. Isso pode levar um bom tempo.")
        print("\r[!] Nao use o computador enquanto a geracao estiver sendo realizada." )
        print("\n------------------------------------------------------\n"             )
        startCodesGenerate = datetime.now()
        while True:
            p = 0
            fTextName = "comments.txt"
            while os.path.exists(fTextName):
                p += 1
                fTextName = "comments" + "(" + str(p) + ")" + ".txt"

            with open(fTextName, 'a') as arquive:
                try:
                    for comment in comments['comments']:
                        i += 1
                        # -----------------
                        # get informations
                        # -----------------
                        comment_owner = "@" + str(comment.owner.username)
                        comment_content = str(comment.text)

                        # ---------------
                        # put in arrays
                        # ---------------
                        users.append(comment_owner)
                        comments_getted.append(comment_content)

                        # put on txt
                        arquive.write("\r---------------------" + "\n" + "comment number => " + str(i) + "\n" + "username => " + str(comment_owner) + "\n" + "comment => " + str(comment_content) + "\n" + "---------------------" + "\n \n")
                        print("\rDados do comentario " + str(i) + " obtido com sucesso")
                except Exception as e:
                    print(e)
                    i -= 1
                    print(    "\n------------------------------------------------------\n"       )
                    print(    "\r[x] Ocorreu um erro durante a geracao do codigo do comentario " + str(i) )
                    print(    "\n------------------------------------------------------\n"       )
                    continue
                arquive.close()
            break
        endCodesGenerate = datetime.now()
        print( "\n------------------------------------------------------\n"              )
        print( "\r[+] Dados extraidos com sucesso" )
        print( "\r[!] Iniciando montagem da planilha. Isso pode levar um bom tempo."     )
        print( "\r[!] Nao use o computador enquanto a montagem estiver sendo realizada." )
        print( "\n------------------------------------------------------\n"              )

        # ------------------
        # export datas
        # ------------------
        users.pop(0)
        comments_getted.pop(0)

        k = 0
        startConstructTable = datetime.now()
        while True:
            k += 1
            try:
                instagramScraper.excel_exporter(users, comments_getted, self)
                print("\n------------------------------------------------------\n"              )
                print("\r[+] Planilha montada com sucesso" )
                print("\rVoce pode visualiza-la em => " + str(self.fname) )
                print("\n------------------------------------------------------\n"              )
                constructTable = True
            except Exception as e:
                if(int(k) > int(5)):
                    print(    "\n------------------------------------------------------\n"       )
                    print(    "\r[x] Excesso de tentativas na montagem da planilha\nFinalizando script..."  )
                    print(    "\n------------------------------------------------------\n"       )
                    constructTable = False
                    pass
                    break
                else:
                    print(    "\n------------------------------------------------------\n"       )
                    print(    "\r[x] Nao foi possivel montar a planilha\nVamos tentar novamente..."  )
                    print(    "\n------------------------------------------------------\n"       )
                    continue
            break
        endConstructTable = datetime.now()
        # -----------
        # show logs
        # -----------
        end = datetime.now().strftime("%d/%m/%Y %H:%M")
        endExecution = datetime.now()
        executionTime =  endExecution - self.start
        extractCommentsTime = endExtractCommentsTime - startExtractCommentsTime
        codesGenerateTime = endCodesGenerate - startCodesGenerate
        print("\n------------------------------------------------------\n"                  )
        print("\r[!] LOGS\n"                                                                 )
        print("\r[!] Comentarios obtidos => "     + str(i)                                   )
        print("\r[!] Deveriam ser obtidos => "    + str(self.qtdComments)                    )
        print("\r[!] Inicio => "      + str(self.start.strftime("%d/%m/%Y %H:%M"))           )
        print("\r[!] Termino => "     + str(end)                                             )
        print("\r[!] Tempo de extracao dos comentarios => " + str(extractCommentsTime)       )
        print("\r[!] Tempo de extracao de dados dos comentarios => " + str(codesGenerateTime))
        if(constructTable):
            constructTableTime = endConstructTable - startConstructTable
            print("\r[!] Tempo de montagem da planilha => " + str(constructTableTime)        )
        print("\r[!] Tempo total de execucao => " + str(executionTime)                       )
        print( "\n------------------------------------------------------\n"                  )
        input("Pressione qualquer tecla para encerrar")
# -------------------
# start bot
# -------------------
bot = instagramScraper()
bot.scraper()