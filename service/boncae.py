import requests


async def find_boncae(name,key):

    headers = {
        "x-nxopen-api-key":key
    }
    urlString = 'https://open.api.nexon.com/maplestory/v1/id?character_name='+name
    response = requests.get(urlString, headers = headers)
    userocid=response.json()['ocid']
    urlString2 ='https://open.api.nexon.com/maplestory/v1/ranking/union?date=2023-12-22&ocid='+userocid
    response = requests.get(urlString2, headers = headers)
    boncae_name =response.json()['ranking'][0]['character_name']
    return boncae_name
