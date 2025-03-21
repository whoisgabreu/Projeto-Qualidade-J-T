# import requests


# {
#     "id": "771017033398624289",
#     "networkId": 137,
#     "networkCode": "310000",
#     "networkName": "MG",
#     "jobName": "Exportar carta de porte de entrega20250321102525-90009999",
#     "modelName": "Operação de estação-Exportar cartas de porte de entrega",
#     "modelType": "dispatchWaybillSite",
#     "statusType": 1,
#     "fileUrl": "aza30del/yl-networkft-api/dispatchWaybillSite771017388391927816/20250321/Exportar+carta+de+porte+de+entrega20250321102525-90009999-90009999.XLSX",
#     "createBy": 38255,
#     "createByName": "Gabriel Lucas de Ângelus",
#     "createTime": "2025-03-21 10:25:25",
#     "updateBy": 38255,
#     "updateByName": "Gabriel Lucas de Ângelus",
#     "updateTime": "2025-03-21 10:25:25",
#     "fileGenerateTime": "2025-03-21 10:26:50",
#     "version": 1,
#     "sort": 0
# }

# "https://gw.jtjms-br.com/networkmanagement/ft/ftExport/pageBalance"

# params = {
#     'current':1,
#     'size':20,
#     'total':2,
#     'operatorCode':'90009999',
#     'jobName':None,
#     'operatingStartTime':'2025-03-21+00:00:00',
#     'operatingEndTime':'2025-03-21+23:59:59'
# }

# "https://gw.jtjms-br.com/networkmanagement/file/downloadFile?path=aza30del%2Fyl-networkft-api%2FdispatchWaybillSite771017388391927816%2F20250321%2FExportar+carta+de+porte+de+entrega20250321102525-90009999-90009999.XLSX"

# # Provalmente não vai funcionar


# # token = "2261f7aba51a4150b3695151df29bd1d"

# # url = "https://gw.jtjms-br.com/servicequality/problemPiece/registrationPage"

# # header = {
# #     "Accept": "application/json, text/plain, */*",
# #     "Accept-Encoding": "gzip, deflate, br, zstd",
# #     "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
# #     "Cache-Control": "max-age=2, must-revalidate",
# #     "Connection": "keep-alive",
# #     "Content-Type": "application/json;charset=UTF-8",
# #     "Host": "gw.jtjms-br.com",
# #     "Origin": "https://jmsbr.jtjms-br.com",
# #     "Referer": "https://jmsbr.jtjms-br.com/",
# #     "Sec-Fetch-Dest": "empty",
# #     "Sec-Fetch-Mode": "cors",
# #     "Sec-Fetch-Site": "same-site",
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
# #     "authToken": token,
# #     "lang": "PT",
# #     "langType": "PT",
# #     "routeName": "problemPieceQuery",
# #     "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
# #     "sec-ch-ua-mobile": "?0",
# #     "sec-ch-ua-platform": "\"Windows\"",
# # }

# # payload = {
# #     "current":1,
# #     "size":9999,
# #     "problePieceStatus":"",
# #     "startTime":"2025-03-01 00:00:00",
# #     "endTime":"2025-03-21 23:59:59",
# #     "countryId":"1"
# #     }

# # response = requests.post(url = url, headers = header, json = payload)

# # print(response.json()["data"]["pages"])

import json
with open("config.json", "r") as config:
    config = json.load(config)

    config["user"]
    