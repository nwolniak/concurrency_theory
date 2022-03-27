import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.Semaphore;


public class NPhilosophersArbiter {
    private final int n;
    private final Semaphore arbiter;
    private final Semaphore[] forks;
    private final Thread[] philosophers;
    private final int feedingCounter;
    private double waitingTime;
    private final double[] avgTimes;
    private FileWriter writer;


    public NPhilosophersArbiter(int n, int feedingCounter) {
        this.n = n;
        this.arbiter = new Semaphore(this.n - 1); // tylko n - 1 filozofow (zasobów) dla arbitra
        this.forks = new Semaphore[this.n];
        for (int i = 0; i < this.n; i++) {
            this.forks[i] = new Semaphore(1); // when there is a fork its 1 else 0
        }
        this.philosophers = new Thread[this.n];
        this.feedingCounter = feedingCounter;
        this.waitingTime = 0;
        this.avgTimes = new double[this.n];

        try {
            this.writer = new FileWriter(String.format("C:\\Users\\Norbert\\Desktop\\tw\\lab2\\%s%d.csv", "arbiter", this.n));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void runArbiterSim() {
        for (int i = 0; i < this.n; i++) {
            int finalI = i;
            this.philosophers[i] = new Thread(new Runnable() {
                @Override
                public void run() {
                    for (int j = 0; j < feedingCounter; j++) {
                        // arbiter acquire
                        try {
                            arbiter.acquire();
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        // philosopher
                        do {
                            myslenie(finalI);
                        } while (!sprobojPodniescObaWidelce(finalI));
                        jedzenie(finalI);
                        odlozObaWidelce(finalI);

                        // arbiter release
                        arbiter.release();
                    }
                    avgTimes[finalI] = getAverageTime();
                }
            });
            this.philosophers[i].start();
        }

        for (int i = 0; i < this.n; i++) {
            try {
                this.philosophers[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        // write times to csv
        try {
            writer.append(String.format("%s,%s\n", "Philosopher", "Time[ms]"));
            for (int i = 0; i < this.n; i++) {
                writer.append(String.format("%d,%d\n", i + 1, (int) this.avgTimes[i]));
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("Koniec");
    }

    public synchronized boolean sprobojPodniescObaWidelce(int i) {
        if (this.forks[i].tryAcquire()) {
            if (this.forks[(i + 1) % this.n].tryAcquire()) {
                return true;
            } else {
                this.forks[i].release();
            }
        }
        return false;
    }

    public synchronized void odlozObaWidelce(int i) {
        this.forks[i].release();
        this.forks[(i + 1) % this.n].release();
    }

    public synchronized void myslenie(int i) {
        System.out.println("Myślę : " + i);
        try {
            this.waitingTime += 100;
            this.wait(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public synchronized void jedzenie(int i) {
        System.out.println("Jem : " + i);
        try {
            this.wait(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public double getAverageTime() {
        return this.waitingTime / (double) this.feedingCounter;
    }

}
