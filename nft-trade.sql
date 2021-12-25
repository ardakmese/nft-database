create database nft;
use nft;

drop table if exists ParaBirim;
create table ParaBirim (
   id INTEGER PRIMARY KEY NOT NULL,
   ParaBirim char (20)
);

insert into ParaBirim values (1,'Btc');
insert into ParaBirim values (2,'Eth');
insert into ParaBirim values (3,'Doge');
insert into ParaBirim values (4,'Abc');

drop table if exists Tamamlanma;
create table Tamamlanma (
    id int(10) not null auto_increment primary key,
    Tamamlanma char(30)
);
insert into Tamamlanma values (NULL,'Tamamlandi');
insert into Tamamlanma values (NULL,'Hatali_Aktarim');


drop table if exists Kategori;
create table Kategori (
    id int(10) not null auto_increment primary key,
    name char(30)
);
insert into Kategori values (NULL,'Sanat');
insert into Kategori values (NULL,'Muzik');
insert into Kategori values (NULL,'Spor');
insert into Kategori values (NULL,'Web3');


drop table if exists NftUrun;
create table NftUrun (
    id int(10) not null auto_increment primary key,
    urun_adi char(30),
    urun_fiyat int(20),
    urun_para_birim int(10),
    CONSTRAINT fk_urun_parabirim_id FOREIGN KEY (urun_para_birim)
    REFERENCES ParaBirim(id),
    urun_kategori_id int(10),
    CONSTRAINT fk_urun_kategori_id FOREIGN KEY (urun_kategori_id)
    REFERENCES Kategori(id)
);

insert into NftUrun values (NULL,'Christmas Card',50,1,4);
insert into NftUrun values (NULL,'iCat',60,2,3);
insert into NftUrun values (NULL,'CryptoPig',70,3,2);
insert into NftUrun values (NULL,'Satoshi Nakamoto',80,4,1);
insert into NftUrun values (NULL,'adidas Nft',90,2,4);
insert into NftUrun values (NULL,'Cem Yılmaz',290,3,2);


drop table if exists Cuzdan;
create table Cuzdan (
    id int(10) not null auto_increment primary key,
    para_miktari int(30) unsigned not null,
    para_birimi_id int(10),
    nft_urun_id int(10),
    CONSTRAINT fk_para_birimi_id FOREIGN KEY (para_birimi_id)
    REFERENCES ParaBirim(id),
    CONSTRAINT fk_nft_urun_id FOREIGN KEY (nft_urun_id)
    REFERENCES NftUrun(id)
);

#müşteriler cüzdan
insert into Cuzdan values (NULL,100,1,NULL);
insert into Cuzdan values (NULL,200,2,NULL);
insert into Cuzdan values (NULL,300,3,NULL);

#satıcılar cüzdan
insert into Cuzdan values (NULL,10,1,1);
insert into Cuzdan values (NULL,20,2,2);
insert into Cuzdan values (NULL,30,3,3);
insert into Cuzdan values (NULL,10,1,4);
insert into Cuzdan values (NULL,20,2,5);
insert into Cuzdan values (NULL,30,3,6);


drop table if exists Musteri;
create table Musteri (
   id int(10) not null auto_increment primary key,
   musteri_adi char (30),
   musteri_soyadı char(30),
   mail_adress char(50),
   cuzdan_id int(10),
   CONSTRAINT fk_m_cuzdan_id FOREIGN KEY (cuzdan_id)
   REFERENCES Cuzdan(id)
);

insert into Musteri values(NULL,'Arda','Akmeşe','akmese21@itu.edu.tr',3);
insert into Musteri values(NULL,'Mehmet','Kripto','mehmet21@itu.edu.tr',2);
insert into Musteri values(NULL,'Ahmet','Web3','ahmet21@itu.edu.tr',1);

drop table if exists Satici;
create table Satici (
   id int(10) not null auto_increment primary key,
   satici_adi char (30),
   satici_soyadı char(30),
   mail_adress char(50),
   cuzdan_id int(10),
   CONSTRAINT fk_s_cuzdan_id FOREIGN KEY (cuzdan_id)
   REFERENCES Cuzdan(id)
);

insert into Satici values(NULL,'Veli','Can','velican@gmail.com',4);
insert into Satici values(NULL,'Cryoto','Seller','crypto@gmail.com',5);
insert into Satici values(NULL,'Nft','Seller','nftseller@gmail.com',6);
insert into Satici values(NULL,'Web3','Seller','web3@gmail.com',7);
insert into Satici values(NULL,'Adidas','Orijinal','adidas@gmail.com',8);
insert into Satici values(NULL,'Cem','Yılmaz','cmylmz@gmail.com',9);


drop table if exists Satış;
create table Satış(
   id int(10) not null auto_increment primary key,
   satış_fiyatı int(30),
   satış_para_birimi_id int(10),
   satış_nft_urun_id int(10),
   satış_tamamlanma_id int(10),
   satış_alıcı_id int(10),
   satış_satıcı_id int(10),
   satış_tarihi TIME,
   CONSTRAINT fk_satis_para_birimi_id FOREIGN KEY (satış_para_birimi_id)
   REFERENCES ParaBirim(id),
   CONSTRAINT fk_satıs_nft_urun_id FOREIGN KEY (satış_nft_urun_id)
   REFERENCES NftUrun(id),
   CONSTRAINT fk_tamamlanma_id FOREIGN KEY (satış_tamamlanma_id)
   REFERENCES Tamamlanma(id),
   CONSTRAINT fk_satıs_alici_id FOREIGN KEY (satış_alıcı_id)
   REFERENCES Musteri(id),
   CONSTRAINT fk_satıs_satici_id FOREIGN KEY (satış_satıcı_id)
   REFERENCES Satici(id)
);
