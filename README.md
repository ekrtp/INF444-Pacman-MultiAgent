# INF444 - Pac-Man Multi-Agent Search

Bu proje, Galatasaray Üniversitesi Bilgisayar Mühendisliği Bölümü **INF444 - Yapay Zeka** dersi kapsamında geliştirilmiştir. Berkeley CS188 Pac-Man projesinin "Multi-Agent Search" modülünü içerir.

**Proje Ekibi:**
* Emirhan Karatepe
* S.T. Burak Altındal

## Proje Hakkında
Bu projede, Pac-Man oyununda hayaletlere karşı optimal (veya rasyonel) kararlar verebilen ajanlar tasarlanmıştır. Proje detayı için: https://inst.eecs.berkeley.edu/~cs188/fa25/projects/proj2/

Tamamlanan Görevler:
1.  **Soru 4:** Expectiminimax Algoritması (Rastgele hareket eden hayaletler için).
2.  **Soru 5:** Gelişmiş Değerlendirme Fonksiyonu (Better Evaluation Function).

## Kurulum ve Çalıştırma

Gerekli dosyalar `multiAgents.py` içerisindedir. Test etmek için aşağıdaki komutlar kullanılabilir:

### Expectiminimax Testleri

```bash
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3 -q -n 10
python pacman.py -p ExpectimaxAgent -l capsuleClassic -n 3
python pacman.py -p ExpectimaxAgent -l mediumClassic
python pacman.py -p ExpectimaxAgent -l powerClassic
```

### Değerlendirme Fonksiyonu Testi

```bash
python pacman.py -p ExpectimaxAgent -l mediumClassic -a evalFn=better
python autograder.py -q q5
```
