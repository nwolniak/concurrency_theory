public class Main {
    public static void main(String[] args) {
        for (int i = 10 ; i <= 100 ; i+=10)
        {
            System.out.println("\n-----------\n" + i + "\n-----------\n");
            NPhilosophersStarvation starvationSim = new NPhilosophersStarvation(i, 50);
            starvationSim.runStarvationSim();

            NPhilosophersArbiter arbiterSim = new NPhilosophersArbiter(i, 50);
            arbiterSim.runArbiterSim();
        }
    }
}
