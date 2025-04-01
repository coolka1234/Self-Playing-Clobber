# Clobber – Program do gry w Clobber z użyciem Minimax i Alfa-Beta

Opis:  
Program implementuje grę Clobber na planszy o dowolnym rozmiarze (domyślnie 5x6). Obsługuje tryb gry z algorytmem Minimax oraz jego wersję z przycinaniem alfa-beta. Pozwala na wybór heurystyki i głębokości przeszukiwania. W wersji rozszerzonej umożliwia rozgrywkę między dwoma niezależnymi agentami.

Wejście:  
- Plansza w postaci m wierszy po n elementów:  
  B – krążek gracza pierwszego (czarny)  
  W – krążek gracza drugiego (biały)  
  _ – puste pole  
- Parametr `d` – maksymalna głębokość drzewa  
- Wybór heurystyk dla obu graczy (min. 3 różne na gracza)

Wyjście:  
- Reprezentacja końcowego stanu planszy  
- W ostatniej linii: liczba rund i zwycięzca  
- Na stderr: liczba odwiedzonych węzłów i czas działania algorytmu

Tryby działania:  
1. Podstawowy – gracz pierwszy gra optymalnie z użyciem Minimax lub alfa-beta, gracz drugi działa identycznie  
2. Rozszerzony – dwóch niezależnych agentów, każdy z własną strategią i możliwością zmiany heurystyki w trakcie gry
