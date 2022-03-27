public class Counter {
    private int counter;
    private final BinarySemaphore binarySemaphore;
    private final InvalidBinarySemaphore invalidBinarySemaphore;
    private final CountingSemaphore countingSemaphore;

    public Counter(){
        this.counter = 0;
        this.binarySemaphore = new BinarySemaphore();
        this.invalidBinarySemaphore = new InvalidBinarySemaphore();
        this.countingSemaphore = new CountingSemaphore(1);
    }

    public void Race(){
        this.counter = 0;
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    binarySemaphore.P();
                    increment();
                    binarySemaphore.V();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    binarySemaphore.P();
                    decrement();
                    binarySemaphore.V();
                }
            }
        });

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Counter binary (while) : " + this.counter);

    }

    public void RaceInvalid(){
        this.counter = 0;
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    invalidBinarySemaphore.P();
                    increment();
                    invalidBinarySemaphore.V();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    invalidBinarySemaphore.P();
                    decrement();
                    invalidBinarySemaphore.V();
                }
            }
        });

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Counter binary (if): " + this.counter);
    }

    public void RaceCounting(){
        this.counter = 0;
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    countingSemaphore.P();
                    increment();
                    countingSemaphore.V();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0 ; i < 100000 ; i++){
                    countingSemaphore.P();
                    decrement();
                    countingSemaphore.V();
                }
            }
        });

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Counter counting : " + this.counter);
    }


    private void increment(){
        this.counter += 1;
    }

    private void decrement(){
        this.counter -= 1;
    }

}
