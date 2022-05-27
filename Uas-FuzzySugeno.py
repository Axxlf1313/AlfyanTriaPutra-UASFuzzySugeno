#Nama   : Alfyan Tria Putra
#NIM    : 191011401794
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : Permintaan Pencucian Galon Air Minum

#Kecepatan Debit Air : min 2 liter/detik dan max 4 liter/detik.
#Banyaknya Galon  : sedikit 50 dan banyak 150.
#Tingkat Kekotoran Galon : rendah 20, sedang 30, dan 40 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Galon():
    minimum = 50
    maximum = 150

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kotor():
    minimum = 20
    medium = 30
    maximum = 40

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Debit():
    minimum = 2
    maximum = 4
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_Galon, jumlah_kotor):
        gln = Galon()
        ktr = Kotor()
        result = []
        
        # [R1] Jika Galon SEDIKIT, dan Kotor RENDAH, 
        #     MAKA Debit = 2
        α1 = min(gln.sedikit(jumlah_Galon), ktr.rendah(jumlah_kotor))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Galon SEDIKIT, dan Kotor SEDANG, 
        #     MAKA Debit = 10 * jumlah_kotor + 100
        α2 = min(gln.sedikit(jumlah_Galon), ktr.sedang(jumlah_kotor))
        z2 = 10 * jumlah_kotor + 100
        result.append((α2, z2))

        # [R3] Jika Galon SEDIKIT, dan Kotor TINGGI, 
        #     MAKA Debit = 10 * jumlah_kotor + 200
        α3 = min(gln.sedikit(jumlah_Galon), ktr.tinggi(jumlah_kotor))
        z3 = 10 * jumlah_kotor + 200
        result.append((α3, z3))

        # [R4] Jika Galon BANYAK, dan Kotor RENDAH,
        #     MAKA Debit = 5 * jumlah_Galon + 2 * jumlah_kotor
        α4 = min(gln.banyak(jumlah_Galon), ktr.rendah(jumlah_kotor))
        z4 = 5 * jumlah_Galon + 2 * jumlah_kotor
        result.append((α4, z4))

        # [R5] Jika Galon BANYAK, dan Kotor SEDANG,
        #     MAKA Debit = 5 * jumlah_Galon + 4 * jumlah_kotor + 100
        α5 = min(gln.banyak(jumlah_Galon), ktr.sedang(jumlah_kotor))
        z5 = 5 * jumlah_Galon + 4 * jumlah_kotor + 100
        result.append((α5, z5))

        # [R6] Jika Galon BANYAK, dan Kotor TINGGI,
        #     MAKA Debit = 5 * jumlah_Galon + 5 * jumlah_kotor + 300
        α6 = min(gln.banyak(jumlah_Galon), ktr.tinggi(jumlah_kotor))
        z6 = 5 * jumlah_Galon + 5 * jumlah_kotor + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_Galon, jumlah_kotor):
        inferensi_values = self.inferensi(jumlah_Galon, jumlah_kotor)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])