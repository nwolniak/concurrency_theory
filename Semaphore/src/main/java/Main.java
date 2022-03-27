public class Main {
    public static void main(String[] args) {
        Counter myCounter = new Counter();
        // używając pętli while w semaforze, obudzony wątek sprawdzi przed wyjściem z pętli
        // warunek co uniemożliwia wielu wątkom opuszczenie pętli i jednoczesne wejście do
        // sekcji krytycznej

        myCounter.Race(); // stan licznika na koniec = 0

        // używając if , każdy obudzony wątek zmieni wartość semafora oraz co za tym idzie
        // wejdzie do sekcji krytycznej

        myCounter.RaceInvalid(); // stan licznika na koniec != 0

        // Semafor binarny jest szczególnym przypadkiem semafora licznikowego,
        // ponieważ semafor binarny może przyjąć dwie wartości {0,1} a semafor licznikowy
        // przyjmuje wartości całkowitoliczbowe
        // do implementacji semafora licznikowego użyłem dwóch semaforów binarnych
        // jeden semafor służy do udostępniania zasobu wątkom a drugi semafor do działań na wewnętrznym liczniku

        myCounter.RaceCounting(); // stan licznik na koniec = 0

    }
}
