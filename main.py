from modules.Start_App import Get_Token
import os
import datetime
import schedule
import time

def main_func():

    os.system("cls")

    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"-----------------\nIniciado {hora}\n-----------------")

    try:

        authtoken = Get_Token().start()
        if authtoken:


            print("-----------------\nDados atualizados com sucesso!\n-----------------")
        
        else:
            print("-----------------\nFalha ao coletar Token.\n-----------------")
    
    except Exception as e:
        print(f"-----------------\nErro na execução. Aguarde nova iteração.\n-----------------{e}")




schedule.every().day.at("07:20").do(main_func)
schedule.every().day.at("11:20").do(main_func)
schedule.every().day.at("13:20").do(main_func)
schedule.every().day.at("15:20").do(main_func)
schedule.every().day.at("19:20").do(main_func)

main_func()

while True:
    schedule.run_pending()
    time.sleep(30)