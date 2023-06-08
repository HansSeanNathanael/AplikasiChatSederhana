# Dokumentasi Protokol

Protokol v1.3 (14:25 - 8 Juni 2023)

## Format id 

ID menggunakan format menyerupai email dan domain yang digunakan adalah:
```text
@kelompok6.co.id
```

sehingga contoh format id adalah seperti
```text
contoh_saja@kelompok6.co.id
```

## Aturan protokol

Peraturan aplikasi
1. ID user harus menggunakan format email.
2. ID grup harus menggunakan format email.

Perlu diperhatikan aturan protokol yang harus dipenuhi agar program berjalan dengan baik.
1. Request dalam bentuk string
2. Menggunakan CRLF (\r\n) untuk membagi bagian-bagian dari data yang dikirimkan
3. Data yang dikirimkan diakhiri oleh 2 CRLF (\r\n\r\n)
4. Untuk respon dari server berupa JSON

Perlu dipehatikan juga cara membaca dokumentasi.
> REGISTER awalan_id password
1. Untuk keyword pada data socket ditulis dengan huruf kapital (contohnya REGISTER).
2. Parameter masukan ditulis dengan huruf kecil (contohnya awalan_id dan password).
3. Setiap sub bagian data yang dikirim dipisahkan oleh CRLF, bila pada contoh di atas seharusnya " " (spasi) adalah CRLF



## daftar protokol
1. [Untuk internal](#protokol-untuk-internal)
2. [Untuk realm eksternal](#protokol-untuk-realm-eksternal)



## Protokol untuk Internal

Protokol ini diperuntukkan kebutuhan internal realm. Protokol untuk realm eksternal terdapat di [sini](#protokol-untuk-realm-eksternal).

Daftar protokol
1. [Membuat akun](#membuat-akun)
2. [Login](#login)
3. [Logout](#logout)
4. [Membuat Group](#membuat-group)
5. [Gabung Group](#gabung-group)
6. [Keluar Group](#keluar-group)
7. [Mengirim chat](#mengirim-chat)
8. [Mengirim file](#mengirim-file)
9. [Mengambil inbox](#mengambil-inbox)
10. [Chat masuk](#chat-masuk)



### Membuat akun

Untuk request membuat akun baru dari klien. Berikut adalah formatnya:
```text
REGISTER awalan_id password
```

Penjelasan parameter:
- awalan_id : untuk id dari akun berupa string. Nantinya awalan id akan ditambahkan dengan domain dari server ini menjadi id yang lengkap (Mirip seperti ketika membuat email Google di mana kita memilih prefix id email tetapi ditambahkan @gmail.com oleh google).
- password : password untuk akun yang dibuat

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - id_akun : id dari akun (dapat dilihat hasilnya dari penjelasan parameter)

2. Bila gagal:
    - error : pesan gagal



### Login

Untuk request login dengan mengirimkan data ke server dan server harus merespon dengan sebuah token autentikasi yang akan digunakan pada sebagian request yang harus terautentikasi. Berikut adalah formatnya:
```text
LOGIN id_akun password
```

Penjelasan parameter:
- id_akun : id dari akun
- password : password akun tersebut

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - token : token autentikasi yang nantinya akan digunakan untuk sebagian request yang mengharuskan sudah terautentikasi

2. Bila gagal:
    - error : pesan gagal



### Logout

Untuk request logout. Logout hanya bisa bila telah login sehingga membutuhkan token autentikasi untuk logout. Berikut adalah formatnya:
```text
LOGOUT token
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil

2. Bila gagal:
    - error : pesan gagal



### Membuat Group

Untuk membuat group chat. Group chat berisi sekumpulan user dapat dari realm internal dan juga realm eksternal. Sebuah group chat akan memiliki id sepert id akun dan password (dapat kosong) untuk user begabung ke dalam grup. Hanya anggota grup saja yang dapat mengirimkan chat. Berikut adalah formatnya:
```text
BUAT_GRUP token awalan_id password 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena membuat grup hanya dapat dilakukan bila memiliki akun
- awalan_id : id awalan dari id grup
- password : password untuk grup (dapat kosong)

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - id_grup : id dari grup

2. Bila gagal:
    - error : pesan gagal



### Gabung Group

Untuk bergabung dengan sebuah grup chat yang berada pada realm internal dan realm eksternal bila didukung oleh realm lain. Berikut adalah formatnya:
```text
GABUNG_GRUP token id_grup password 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena bergabung grup hanya dapat dilakukan bila memiliki akun
- id_grup : id grup tujuan
- password : password untuk bergabung dengan sebuah grup. (Bila bergabung dengan grup di luar realm dan tidak ada fitur maka dapat dibiarkan kosong)

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil

2. Bila gagal:
    - error : pesan gagal



### Keluar Group

Untuk keluar dari sebuah grup chat yang berada pada realm internal atau realm eksternal bila didukung oleh realm lain. Berikut adalah formatnya:
```text
KELUAR_GRUP token id_grup 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena keluar dari sebuah grup hanya dapat dilakukan bila memiliki akun
- id_grup : id grup tersebut

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil

2. Bila gagal:
    - error : pesan gagal



### Mengirim chat

Untuk mengirim chat ke user lain di dalam realm internal atau menuju user yang berada di realm eksternal. Berikut adalah format untuk mengirim chat:
```text
CHAT token id_tujuan isi_chat 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena mengirim hanya dapat dilakukan bila memiliki akun
- id_tujuan : id lawan bicara (dapat personal atau grup)
- isi_chat : chat yang dikirimkan

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal



### Mengirim file

Untuk mengirim file ke user lain di dalam realm internal atau menuju user yang berada di realm eksternal. Berikut adalah format untuk mengirim file:
```text
FILE token id_tujuan nama_file isi_file 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena mengirim hanya dapat dilakukan bila memiliki akun
- id_tujuan : id lawan bicara (dapat personal atau grup)
- nama_file : nama dari file yang dikirimkan
- isi_file : isi file dalam format base64

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal



### Mengambil inbox

Untuk mengambil isi chat yang terdapat di dalam inbox. Chat yang sudah diambil akan dihapus sehingga menjadi tanggung jawab aplikasi klien untuk menyimpan data dalam basis data. Berikut adalah format untuk mengambil isi inbox:
```text
INBOX token 
```

Penjelasan parameter:
- token : token autentikasi yang didapat saat login karena mengambil inbox hanya dapat dilakukan bila memiliki akun


Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    akan berisi JSON dengan setiap attribute/key adalah alamat asal pengirim dan nilainya adalah array message. Bentuk JSON message adalah sebagai berikut:
    - id_tujuan : id dari tujuan
    - id_pengirim : id dari pengirim chat
    - keperluan : keperluan ada "PRIVATE" atau "GRUP"  
    - bentuk_chat : bentuk chat ada dua yaitu "CHAT" atau "FILE"
    - id_grup : id dari grup bila chat dikirimkan menuju grup
    - chat : hanya ada bila bentuk_chat adalah CHAT. Isinya adalah chat yang dikirim.
    - nama_file : hanya ada bila bentuk_chat adalah FILE. Isinya adalah nama file yang dikirim.
    - isi_file : hanya ada bila bentuk_chat adalah FILE. Isinya adalah isi file yang dikirim dalam format base64.
    - tanggal_diterima : tanggal diterimanya data pada server

2. Bila gagal:
    - error : pesan gagal



### Chat masuk

Ini bukanlah request tetapi ini adalah data chat yang dikirimkan oleh server secara real time ketika user online. Menjadi tanggung jawab aplikasi klien untuk menyimpan data chat ke dalam database. Server akan meneruskan tanpa menyimpan data ke dalam basis data. 

Chat dikirim dalam bentuk JSON. Format JSON chat adalah sebagai berikut:
- id_tujuan : id dari tujuan
- id_pengirim : id dari pengirim chat
- keperluan : keperluan ada "PRIVATE" atau "GRUP"  
- bentuk_chat : bentuk chat ada dua yaitu "CHAT" atau "FILE"
- id_grup : id dari grup bila chat dikirimkan menuju grup
- chat : hanya ada bila bentuk_chat adalah CHAT. Isinya adalah chat yang dikirim.
- nama_file : hanya ada bila bentuk_chat adalah FILE. Isinya adalah nama file yang dikirim.
- isi_file : hanya ada bila bentuk_chat adalah FILE. Isinya adalah isi file yang dikirim dalam format base64.
- tanggal_diterima : tanggal diterimanya data pada server



## Protokol untuk Realm Eksternal

Protokol ini diperuntukkan kebutuhan realm eksternal yang ingin mengintegrasikan aplikasi mereka agar dapat berkomunikasi dengan aplikasi ini.

Daftar protokol
1. [Gabung Group](#gabung-group-eksternal)
2. [Keluar Group](#keluar-group-eksternal)
3. [Mengirim chat](#mengirim-chat-eksternal)
4. [Mengirim file](#mengirim-file-eksternal)
5. [Mengirim chat group](#mengirim-chat-eksternal)
6. [Mengirim file group](#mengirim-file-eksternal)
7. [Autentikasi Realm Eksternal]() *Masih didiskusikan*



### Gabung Group [Eksternal]

Untuk bergabung dengan sebuah grup chat. Berikut adalah formatnya:
```text
GABUNG_GRUP_EKSTERNAL id_user id_grup password 
```

Penjelasan parameter:
- id_user : id dari user eksternal yang ingin bergabung. ID user harus menyerupai format email agar dapat bekerja.
- id_grup : id grup tujuan.
- password : password untuk bergabung dengan sebuah grup. (Dapat kosong bila grup tidak memiliki password)

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil

2. Bila gagal:
    - error : pesan gagal



### Keluar Group [Eksternal]

Untuk keluar dari sebuah grup chat. Berikut adalah formatnya:
```text
KELUAR_GRUP_EKSTERNAL id_user id_grup
```

Penjelasan parameter:
- id_user : id dari user eksternal yang ingin keluar dari grup.
- id_grup : id grup tersebut

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil

2. Bila gagal:
    - error : pesan gagal



### Mengirim chat [Eksternal]

Untuk mengirim chat baik secara personal atau menuju alamat grup pada realm kami. Peringatan! Untuk chat yang dikirim hanya akan diteruskan ke semua anggota selain pengirim sehingga menjadi tanggung jawab anda untuk menyimpan pesan yang dikirim untuk sang pengirim. Request ini juga hanya diperuntukkan mengirim chat private menuju user atau grup pada realm kami. Untuk meneruskan chat grup dari realm anda menuju user realm kami gunakan [mengirim chat grup eksternal](#mengirim-chat-group-eksternal). Berikut adalah format untuk mengirim chat:
```text
CHAT_EKSTERNAL id_pengirim id_tujuan isi_chat 
```

Penjelasan parameter:
- id_pengirim : id dari pengirim eksternal
- id_tujuan : id lawan bicara (dapat personal atau grup)
- isi_chat : chat yang dikirimkan

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal



### Mengirim file [Eksternal]

Untuk mengirim file menyerupai [mengirin chat eksternal](#mengirim-chat-eksternal). Berikut adalah format untuk mengirim file:
```text
FILE_EKSTERNAL id_pengirim id_tujuan nama_file isi_file 
```

Penjelasan parameter:
- id_pengirim : id dari pengirim eksternal
- id_tujuan : id lawan bicara (dapat personal atau grup)
- nama_file : nama dari file yang dikirimkan
- isi_file : isi file dalam format base64

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal


### Mengirim chat group [Eksternal]

Untuk meneruskan chat group dari realm anda menuju user yang berada pada realm kami. Perbedaan dengan [mengirim chat eksternal](#mengirim-chat-eksternal) adalah request ini untuk meneruskan chat dari grup pada realm anda menuju user anggota pada realm kami. Berikut adalah format untuk mengirim chat:
```text
CHAT_GRUP_EKSTERNAL id_pengirim id_tujuan id_grup isi_chat 
```

Penjelasan parameter:
- id_pengirim : id dari pengirim eksternal
- id_tujuan : id lawan bicara (dapat personal atau grup)
- id_grup : id grup realm anda yang terlibat pada chat
- isi_chat : chat yang dikirimkan

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal



### Mengirim file group [Eksternal]

Untuk mengirim file menyerupai [mengirim chat group eksternal](#mengirim-chat-group-eksternal). Berikut adalah format untuk mengirim file:
```text
FILE_GRUP_EKSTERNAL id_pengirim id_tujuan id_grup nama_file isi_file 
```

Penjelasan parameter:
- id_pengirim : id dari pengirim eksternal
- id_tujuan : id lawan bicara (dapat personal atau grup)
- id_grup : id dari grup realm anda yang terlibat
- nama_file : nama dari file yang dikirimkan
- isi_file : isi file dalam format base64

Respon dari server berupa JSON dengan isi:
1. Bila berhasil:
    - success : pesan berhasil
    - waktu_dikirim : menunjukkan kapan pesan berhasil dikirim

2. Bila gagal:
    - error : pesan gagal