#github page: https://github.com/ardakmese/nft-database
#author: Arda Akmeşe

import mysql.connector
import time

query_seller = "select satici_adi, satici_soyadı from satici;"
query_nft = "select urun_adi, urun_fiyat, parabirim.ParaBirim " \
            "from nfturun inner join parabirim on " \
            "nfturun.urun_para_birim = parabirim.id;"

query_completed_sell = "select* from satış;"
query_insert_cuzdan = "insert into Cuzdan values (NULL,{0},{1},NULL);"
query_insert_alici = "insert into Musteri values (NULL, %s, %s, %s, %s);"
query_fetch_cuzdan = "select* from Cuzdan;"

query_find_musteri = "select Musteri.id from Musteri where Musteri.musteri_adi = {};"

query_cuzdan_detail = "select* from Cuzdan where Cuzdan.id = {};"

query_find_owner = "select cuzdan.id from cuzdan " \
                   "inner join satici on satici.cuzdan_id = cuzdan.id " \
                   "inner join nfturun on cuzdan.nft_urun_id = nfturun.id where nfturun.urun_adi = {};"

query_owner_id = "select satici.id from satici where satici.cuzdan_id = {} ;"

query_find_how_much = "select nfturun.urun_fiyat from nfturun where nfturun.urun_adi = {};"

query_update_satici = "UPDATE cuzdan \
SET cuzdan.nft_urun_id = NULL, cuzdan.para_miktari = cuzdan.para_miktari + {0} \
WHERE cuzdan.id = {1};"

query_update_alici = "UPDATE cuzdan \
SET cuzdan.nft_urun_id = {0}, cuzdan.para_miktari = cuzdan.para_miktari - {1} \
WHERE cuzdan.id = {2};"

query_insert_satiş = "insert into Satış values (NULL,{},{},{},{},{},{},{});"


currency = ["btc","eth","doge","abc"]
nft_list = []


def updateNftList():
    nft_list.clear()
    connection = mysql.connector.connect(host='localhost',
                                         database='nft',
                                         user='root',
                                         password='12345678',
                                         auth_plugin='mysql_native_password'
                                         )
    cursor = connection.cursor()
    cursor.execute(query_nft)
    result = cursor.fetchall()
    for row in result:
        nft_list.append(str(row[0]))


def showInDb(input):
    connection = mysql.connector.connect(host='localhost',
                                         database='nft',
                                         user='root',
                                         password='12345678',
                                         auth_plugin='mysql_native_password'
                                         )
    cursor = connection.cursor()
    cursor.execute(input)
    result = cursor.fetchall()
    for i in range(len(result)):
        output = result[i]
        print(output)

    connection.close()



def insertUser():
    user = input("Lütfen kullanıcı adını giriniz: ")
    lastname = input("Lütfen kullanıcı soyadını giriniz: ")
    mail = input("Lütfen mail adresi giriniz: ")
    print(currency)
    user_c = input("Lütfen yukarıdaki listeden seçtiğiniz para birimini yazınız: ")
    while not currency.__contains__(user_c):
        print(currency)
        user_c = input("Yanlış girdiniz, lütfen yukarıdaki listeden seçtiğiniz para birimini yazınız: ")

    amount = input("Lütfen cüzdanınızdaki miktarı giriniz: ")

    connection = mysql.connector.connect(host='localhost',
                                         database='nft',
                                         user='root',
                                         password='12345678',
                                         auth_plugin='mysql_native_password'
                                         )
    cursor = connection.cursor(buffered=True)
    cursor.execute(query_insert_cuzdan.format(amount,currency.index(user_c)+1))
    connection.commit()
    cursor.execute(query_fetch_cuzdan)
    musteriCuzdan = int(len(cursor.fetchall()))
    cursor.execute(query_insert_alici, (user,lastname,mail,musteriCuzdan) )
    connection.commit()

    print("Yeni müşteri {0} adıyla başarıyla tabloya eklendi.".format(user))

    updateNftList()
    print(nft_list)

    userResponse = input("Lütfen gösterilen ürünlerden almak istediğiniz ürünü giriniz: ")
    while not nft_list.__contains__(userResponse):
        print(nft_list)
        userResponse = input("Yanlış girdiniz, lütfen gösterilen ürünlerden almak istediğiniz ürünü giriniz: ")

    cursor.execute(query_find_owner.format("'"+userResponse+"'"))
    res = cursor.fetchone()
    owner_id = res[0]

    cursor.execute(query_cuzdan_detail.format(owner_id))
    res = cursor.fetchall()
    owner_money_id = res[0][2]
    owner_nft_id = res[0][3]

    cursor.execute(query_owner_id.format(owner_id))
    res = cursor.fetchone()
    satici_id = res[0]

    cursor.execute(query_find_how_much.format("'"+userResponse+"'"))
    res = cursor.fetchone()
    current_price = res[0]

    if owner_money_id != currency.index(user_c)+1:
        print("Üzgünüz para birimleri uyuşmuyor, ürün satış birimi: "+ currency[owner_money_id-1]
              + " cüzdanınızdaki birim: "+ user_c)
    elif int(amount) < int(current_price):
        print("Üzgünüz almak istediğiniz item fiyatı: " + str(current_price) +
              " hesabınızdaki nakit: "+ str(amount) )
    else:
        cursor.execute(query_find_musteri.format("'"+user+"'"))
        res = cursor.fetchone()
        musteri_id = res[0]
        zaman = "'"+ time.strftime('%Y-%m-%d %H:%M:%S') + "'"

        cursor.execute(query_update_satici.format(current_price, owner_id))
        connection.commit()
        cursor.execute(query_update_alici.format(owner_nft_id, current_price, musteriCuzdan))
        connection.commit()
        cursor.execute(query_insert_satiş.format(current_price,owner_money_id,owner_nft_id,1,musteri_id,satici_id,zaman))
        connection.commit()
        print("Nft ürününüz hayırlı uğurlu olsun :)")

        showInDb(query_completed_sell)

    startUp()






def startUp():

    user = int(input("Lütfen ilgili sayıyı giriniz; Çıkış [-1], Satıcıları göster [1], Nft ürünleri göster [2], "
                     "Tamamlanmış  satışları göster [3], Nft ürün al [4]: "))
    while True:
        match user:
            case 1:
                showInDb(query_seller)
                startUp()
                break
            case 2:
                showInDb(query_nft)
                startUp()
                break
            case 3:
                showInDb(query_completed_sell)
                startUp()
                break
            case 4:
                insertUser()
                break
            case -1:
                print("Güle güle")
                break

            case _:
                print("Lütfen tekrar giriniz")
                startUp()
                break

startUp()