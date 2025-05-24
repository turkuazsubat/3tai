# 3tai

## Proje Özeti  
3tai, klasik Tic Tac Toe (XOX) oyununun yapay zeka destekli versiyonudur. Kullanıcı dostu arayüzü ve güçlü yapay zekası ile tek kişilik oyun deneyimini zenginleştirir. Minimax algoritması kullanılarak geliştirilmiş yapay zeka, oyuncuya karşı stratejik ve zorlu hamleler yapar.

## Çalışma Prensibi  
3x3'lük tahta üzerinde oyuncu ve yapay zeka sırayla hamle yapar. Amaç, yatay, dikey ya da çaprazda üç aynı sembolü yan yana getirmektir. Yapay zeka, minimax algoritması ile tüm olası hamleleri değerlendirip en avantajlı hamleyi seçer, böylece oyuncuya meydan okur.

## Kullanılan Yapay Zeka Teknikleri  
- **Minimax Algoritması:** Oyun senaryolarını derinlemesine tarar, en iyi hamleyi belirler.  
- **Heuristik Değerlendirme:** Oyun tahtasının durumunu puanlayarak seçim yapmayı optimize eder.  
- **Rastgele Hamle (Düşük Zorluk):** Oyuncunun kolay kazanması için bazı hamleler rastgele seçilir.

## Yapay Zekanın Projedeki Rolü  
Tek oyunculu modda, oyuncunun hamlesi sonrası yapay zeka tahtayı analiz eder ve optimizasyonla en uygun hamleyi yapar. Bu, oyunu gerçekçi ve rekabetçi kılar.
