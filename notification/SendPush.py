import FCMManager as fcm
import mysql.connector
import asyncio

conn = mysql.connector.connect(
    host='mysql-innovit.alwaysdata.net',
    port="3306",
    user='innovit_user',
    password='innovit_pwd',
    database='innovit_smartbev'
)

cur = conn.cursor()


    

async def main(idEntreprise: int) -> None:
    tokens = []
    ids = []
    # write your queries here
    query = "SELECT id FROM users WHERE idEntreprise= "+str(idEntreprise)+" AND idRole =3"
    cur.execute(query)
# Récupération des résultats
    AMS = cur.fetchall()

    for AM in AMS :
        print(AM[0])
        ids.append(AM[0])
    for uid in ids:
        query = "SELECT token FROM tokens WHERE idUser = "+str(uid)
        cur.execute(query)
        toke = cur.fetchone()
        if toke:
            tokens.append(str(toke[0]))


    print(tokens)
    return tokens


if __name__ == '__main__':
    tokens = []
    tokens = asyncio.run(main(1))
    if len(tokens) > 0:
        
        fcm.sendPush("task 4","manque d'eau",tokens)
    else:
        print("gae déconnecté")
