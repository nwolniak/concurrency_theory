public class CountingSemaphore {
    private int _stan;
    private final BinarySemaphore vSemaphore;
    private final BinarySemaphore pSemaphore;

    public CountingSemaphore(int stan){
        this._stan = stan;
        this.vSemaphore = new BinarySemaphore();
        this.pSemaphore = new BinarySemaphore();
    }

    public void V(){
        this.vSemaphore.P(); // semafor binarny dla operacji zwolnienia zasobu
        this._stan += 1;
        if (this._stan > 0) {this.pSemaphore.V();} // gdy zasobów > 0 to odblokuj semafor udostępniający
        this.vSemaphore.V(); // zwolnij semafor po zwolnieniu zasobu
    }

    public void P(){
        this.pSemaphore.P(); // semafor binarny udostępniający zasób wątkowi
        this.vSemaphore.P(); // semafor binarny dla operacji zabrania zasobu
        this._stan -= 1;
        if (this._stan > 0) {this.pSemaphore.V();} // gdy zasobów > 0 to odblokuj semafor udostępniejący
        this.vSemaphore.V(); // zwolnij semafor po zabraniu zasobu
    }

}
