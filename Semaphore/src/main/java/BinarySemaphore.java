public class BinarySemaphore {
    private boolean _stan = true;
    private int _czeka = 0;

    public synchronized void V(){
        this._stan = true;
        this.notify();
    }

    public synchronized void P(){
        while (!this._stan){
            try {
                this.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        this._stan = false;
    }
}
