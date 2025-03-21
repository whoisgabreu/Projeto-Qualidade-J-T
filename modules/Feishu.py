import requests
import json
import os
from feishu_bot import FeishuBot

import asyncio
from PIL import ImageGrab
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

class BIFeishu():
    def __init__(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def PrintarBI_Detalhamento(self,bi_url:str,img_name:str):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium import webdriver
        from feishu_bot import FeishuBot
        import asyncio
        import time
        import datetime
        from webdriver_manager.chrome import ChromeDriverManager
        import keyboard
        import os

        options = webdriver.ChromeOptions()

        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False)

        # Path to Chrome Profile
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Detalhamento")
        options.add_argument(f"user-data-dir={user_data_dir}")
        # Setting the driver path and requesting a page
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(bi_url)

        WebDriverWait(driver,6000,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="visualContainerHost visualContainerOutOfFocus"]')))
        driver.execute_script("""
        document.getElementsByClassName("middleText")[0].click();
        await new Promise(resolve => setTimeout(resolve,2000));
        var lista = document.getElementsByTagName("li");
        for (var i = 0; i < lista.length; i++) {
            if (lista[i].textContent === "Detalhamento") {
                lista[i].getElementsByTagName("button")[0].click();
            }
        }
        await new Promise(resolve => setTimeout(resolve,2000));
        """)
        driver.execute_script('document.body.style.zoom = "80%"')
        time.sleep(3)

        weekday = datetime.datetime.today().weekday()

        if weekday == 5:
            x = 2
        else:
            x = 0

        data = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days = x),"%d/%m/%Y")

        data = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days = x),"%d/%m/%Y")
        # driver.execute_script("""
        # document.getElementsByClassName("date-slicer-control date-slicer-datepicker-wrapper")[1].getElementsByTagName("input")[0].value = arguments[0];
        # document.getElementsByClassName("date-slicer-control date-slicer-datepicker-wrapper")[1].getElementsByTagName("input")[0].dispatchEvent(new Event("input", {bubbles: true, cancelable: true}));
        # document.getElementsByClassName("date-slicer-control date-slicer-datepicker-wrapper")[0].getElementsByTagName("input")[0].value = arguments[0];
        # document.getElementsByClassName("date-slicer-control date-slicer-datepicker-wrapper")[0].getElementsByTagName("input")[0].dispatchEvent(new Event("input", {bubbles: true, cancelable: true}));
        # """,data)
        time.sleep(3)

        # PRINT 1
        img_path = os.path.join(os.path.expanduser('~'), "Documents", img_name+".png")
        # Captura uma imagem maior que o elemento
        driver.save_screenshot("screenshot.png")

        # Abre a imagem completa e recorta a parte desejada
        full_img = Image.open("screenshot.png")
        cropped_img = full_img.crop((92, 0, 92 + 1817, 972))

        # Salva a imagem recortada
        cropped_img.save(img_path)

        # PRINT 2
        img_path = os.path.join(os.path.expanduser('~'), "Documents", img_name+"2.png")
        # Captura uma imagem maior que o elemento
        driver.execute_script('document.getElementsByClassName("visualWrapper report")[13].scrollIntoView();')
        time.sleep(3)
        driver.save_screenshot("screenshot.png")

        # Abre a imagem completa e recorta a parte desejada
        full_img = Image.open("screenshot.png")
        cropped_img = full_img.crop((92, 0, 92 + 1817, 972))

        # Salva a imagem recortada
        cropped_img.save(img_path)

        time.sleep(3)
        driver.quit()


    def gerar_imagem(self,img_dir):
        # Definir escopo correto (Drive apenas)
        scope = ['https://www.googleapis.com/auth/drive.file']

        # Autenticar com as credenciais corretas
        creds_path = os.path.join(os.path.dirname(__file__), "Google API.json")
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        
        # Conectar ao Google Drive
        drive_service = build('drive', 'v3', credentials=creds)

        # Criar metadados do arquivo para upload
        file_metadata = {'name': os.path.basename(img_dir)}
        media = MediaFileUpload(img_dir, mimetype='image/jpeg')

        # Upload do arquivo
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Permitir acesso público
        drive_service.permissions().create(
            fileId=uploaded_file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Retornar link de acesso à imagem
        image_link = f'https://drive.google.com/uc?id={uploaded_file["id"]}'
        
        return image_link

    def enviarMensagem(self,text_msg:str,url_hook:str):

        url = url_hook

        message = {
            "msg_type": "text",
            "content": {
                "text": text_msg
            }
        }


        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(message), headers=headers)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            print('Message sent successfully:', response.text)
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

    def enviarImagem(self,img_name:str,url_hook:str):

        # APP_ID e APP_SECRET
        bot = FeishuBot(app_id="cli_a43c37e7d138d00c",app_secret="jHTiXxjVxTPVKwAsxzAyXkj4dSqhdi7f")

        img_link = self.gerar_imagem(os.path.join(os.path.expanduser('~'),"Documents",img_name))
        img_id = bot.upload_image(img_link)

        url = url_hook

        message = {
            "msg_type": "text",
            "content": {
                "text": "Segue relatório:\nhttps://app.powerbi.com/view?r=eyJrIjoiNTI4ZWJkYjYtZTIzYy00OGE3LTk4NmEtMDk4YjA5MjhlYTI3IiwidCI6IjA4ZjEwZDc2LTgzNTgtNDMxYi05MTI0LWEwMTUxNjI3MDJkYyJ9"
            }
        }

        message2 = {
            "msg_type":"image",
            "content":{
                "image_key": f"{asyncio.run(img_id)}"
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(message2), headers=headers)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            print('Message sent successfully:', response.text)
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")



BIFeishu().PrintarBI_Detalhamento("https://app.powerbi.com/view?r=eyJrIjoiOTAxOWQ4YzItZTMxZS00ZjQ5LWFhNDMtNDdhM2FjOTIyZTk2IiwidCI6IjA4ZjEwZDc2LTgzNTgtNDMxYi05MTI0LWEwMTUxNjI3MDJkYyJ9","detalhamento")
BIFeishu().enviarImagem("detalhamento.png", "https://open.feishu.cn/open-apis/bot/v2/hook/1ff28455-45d6-4ab0-a86d-b2d98a9fe227")