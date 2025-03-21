import requests
import pandas as pd
import time
from io import BytesIO
import datetime

def gestao_de_anormalidade(jms_user, token):

    start_date = datetime.datetime.today().strftime("%Y-%m-01")
    end_date = datetime.datetime.today().strftime("%Y-%m-%d")
    jobName = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4",
    "Cache-Control": "max-age=2, must-revalidate",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=utf-8",
    "Host": "gw.jtjms-br.com",
    "Origin": "https://jmsbr.jtjms-br.com",
    "Referer": "https://jmsbr.jtjms-br.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "authToken": token,
    "lang": "PT",
    "langType": "PT",
    "routeName": "problemPieceQuery",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "timezone": "GMT-0300"
    }

    # Realizar Export
    url = "https://gw.jtjms-br.com/servicequality/problemPiece/exportExcel/sync/all"

    payload = {
        "current":1,
        "size":20,
        "problePieceStatus":"",
        "startTime":f"{start_date} 00:00:00",
        "endTime":f"{end_date} 23:59:59",
        "countryCode":"PT",
        "jobName":f"问题件查询{jobName}",
        "exportType":1,
        "isRegistration":1,
        "isMonitor":False,
        "countryId":"1"}

    requests.post(url = url, headers = header, json = payload)

    # Lista de Download
    url = f"https://gw.jtjms-br.com/servicequality/exportTask/pageBalance?current=1&size=100&total=0&operatorCode={jms_user}&modelType=165&operatingStartTime={end_date}+00:00:00&operatingEndTime={end_date}+23:59:59"

    session = requests.Session()
    session.headers.update(header)

    while True:
        time.sleep(60)
        response = session.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                records = data.get("data", {}).get("records", {})

                if records:
                    ultimo_status = records[0].get("statusType", None)

                    if ultimo_status != 2:
                        fileUrl = records[0]["fileUrl"].replace("/", "%2F").replace(" ", "+")
                        jobNameJson = records[0]["jobName"]
                        break

                    print("status ainda é 2")

            except Exception as e:
                print(e)

    download_url = f"https://gw.jtjms-br.com/servicequality/problemPiece/export/fileUrl?fileName={jobNameJson}&fileUrl={fileUrl}" # Link do Download

    # Realizar o Download
    download = requests.get(url = download_url, headers = header)

    # Fazendo o download
    response = requests.get(download.json()["data"])
    if response.status_code == 200:
        # Carregar a planilha na memória
        xls = pd.ExcelFile(BytesIO(response.content))

        # Verificar as abas disponíveis
        print("Abas disponíveis:", xls.sheet_names)

        # Carregar a primeira aba em um DataFrame
        df = xls.parse(xls.sheet_names[0])

        # Exibir as primeiras linhas
        print(df.head())

        # Salvar uma cópia local
        df.to_excel("dados_processados gestão de anormalidade.xlsx", index=False)
        print("Planilha salva como 'dados_processados.xlsx'.")

    else:
        print(f"Erro ao baixar o arquivo. Código: {response.status_code}")