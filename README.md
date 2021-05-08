# 2. Parkomat

## Opis zadania

- Parkomat przechowuje informacje o monetach/banknotach znajdujących się w
w nim (1, 2, 5, 10, 20, 50gr, 1, 2,5, 10, 20, 50zł)
- Okno z polem tekstowym na numer rejestracyjny pojazdu, aktualną datą (rok, miesiąc, dzień, godzina, minuta), datą wyjazdu z parkingu (rok, miesiąc, dzień, godzina, minuta), przyciskami pozwalającymi na wrzucanie monet (proszę umieścić pole pozwalające wpisać liczbę wrzucanych monet), oraz przyciskiem "Zatwierdź".
- Program powinien zawierać pole pozwalające na przestawienie aktualnego czasu.
- Zasady strefy parkowania:
	- Strefa płatnego parkowania obowiązuje w godzinach od 8 do 20 od poniedziałku do piątku.
	- Pierwsza godzina płatna 2zł.
	- Druga godzina płatna 4zł.
	- Trzecia i kolejne godziny płatne po 5zł.
	- Czas wychodzący poza obowiązywanie płatnego parkowania przechodzi na kolejny dzień
		- Wykupienie godziny parkowania o 19:20 w piątek pozwala na parkowanie do 8:20 w poniedziałek (koniec o 20:20, wychodzi 20 minut poza płatne parkowanie, przechodzi na kolejny płatny dzień).
- Po każdym wrzuceniu monety termin wyjazdu aktualizuje się zgodnie z całą wrzuconą kwotą.
- Jeśli wrzucone zostało mniej pieniędzy niż potrzeba na opłacenie pełnej godziny, to opłacana jest niepełna godzina:
	- Wrzucenie 1zł pozwala na parkowanie 30 minut,
	- Wrzucenie 5zł pozwala na parkowanie 1 godzinę i 45 minut (2zł na opłacenie pierwszej godziny, zostało 3zł, a  potrzeba 4zł na opłacenie kolejnej, co daje 3/4 godziny: 45 minut).
- Po wciśnięciu przycisku "Zatwierdź" wyświetlane jest okno z potwierdzeniem opłacenia parkingu: numer rejestracyjny pojazdu, czas zakupu i termin wyjazdu.
- Numer rejestracyjny może składać się tylko z wielkich liter od A do Z i cyfr.
- W automacie mieści się dowolna liczba banknotów (10, 20, 50zł) i po 200 monet każdego rodzaju. Próba wrzucenia monety ponad limit powoduje wyświetlenie informacji o przepełnieniu parkomatu i prośbę o wrzucenie innego nominału.

## Testy

1. Ustaw niepoprawną godzinę. Oczekiwany komunikat o błędzie. Ustawić godzinę na 12:34.
2. Wrzucić 2zł, oczekiwany termin wyjazdu godzinę po aktualnym czasie. Dorzuć 4zł, oczekiwany termin wyjazdu dwie godziny po aktualnym czasie. Dorzuć 5zł, oczekiwany termin wyjazdu trzy godziny po aktualnym czasie. Dorzuć kolejne 5zł, oczekiwany termin wyjazdu cztery godziny po aktualnym czasie.
3. Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny dzień, zgodnie z zasadami -- wrzucić tyle monet aby termin wyjazdu był po godzinie 19:00, dorzucić monetę 5zł,
4. Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny tydzień, zgodnie z zasadami - wrzucić tyle monet aby termin wyjazdu był w piątek po godzinie 19:00, a potem dorzucić monetę 5zł,
5. Wrzucić 1zł, oczekiwany termin wyjazdu pół godziny po aktualnym czasie,
6. Wrzucić 200 monet 1gr, oczekiwany termin wyjazdu godzinę po aktualnym czasie.
7. Wrzucić 201 monet 1gr, oczekiwana informacja o przepełnieniu parkomatu.
8. Wciśnięcie "Zatwierdź" bez wrzucenia monet -- oczekiwana informacja o błędzie.
9. Wciśnięcie "Zatwierdź" bez wpisania numeru rejestracyjnego -- oczekiwana informacja o błędzie. Wciśnięcie "Zatwierdź" po wpisaniu niepoprawnego numeru rejestracyjnego -- oczekiwana informacja o błędzie.
