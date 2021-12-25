import connectDb
import mysql.connector
import sys

query_seller = "select satici_adi, satici_soyadı from satici;"
query_nft = "select urun_adi from nfturun;"
query_completed_sell = "select* from satış;"
query_insert_cuzdan = "insert into Cuzdan values (NULL,{0},{1},NULL)"
query_insert_alici = "insert into Musteri values (NULL, %s, %s, %s, %s)"
query_fetch_cuzdan = "select* from Cuzdan;"

query_find_owner = "select cuzdan.id \
			from (SELECT * FROM cuzdan) as czdan \
    		inner join satici on satici.cuzdan_id = czdan.id \
    		inner join nfturun on czdan.nft_urun_id = nfturun.id \
    		where nfturun.urun_adi = %s"

query_update_satici = "UPDATE cuzdan \
SET cuzdan.nft_urun_id = NULL, cuzdan.para_miktari = cuzdan.para_miktari + {0} \
WHERE cuzdan.id = {1}"

query_update_alici = "UPDATE cuzdan \
SET cuzdan.nft_urun_id = {0}, cuzdan.para_miktari = cuzdan.para_miktari - {1} \
WHERE cuzdan.id = {2}"

query_insert_satiş = "insert into Satış values (NULL,{},{},{},{},{},{}, %s)"


currency = ["btc","eth","doge","abc"]
nft_list = {}


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
        print(row)


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
    cursor = connection.cursor()
    cursor.execute(query_insert_cuzdan.format(amount,currency.index(user_c)+1),multi=True)
    connection.commit()
    cursor.execute(query_fetch_cuzdan)
    cuzdanSize = len(cursor.fetchall()) + 1
    cursor.execute(query_insert_alici, (user,lastname,mail,cuzdanSize))
    connection.commit()

    print("Yeni müşteri {0} adıyla başarıyla tabloya eklendi.".format(user))

    updateNftList()
    print(tw)
    userResponse = input("Lütfen gösterilen ürünlerden almak istediğiniz ürünü giriniz: ")
    while not nft_list.__contains__(userResponse):
        print(nft_list)
        userResponse = input("Yanlış girdiniz, lütfen gösterilen ürünlerden almak istediğiniz ürünü giriniz: ")


    #
    # if
    #     pass
    # elif amount < kullanıcı parası
    #     pass
    # else:
    #     print("Nft ürününüz hayırlı uğurlu olsun :)")
    #     showInDb(query_completed_sell)

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