#include <iostream>
#include <cmath>

// abstract base scheduler
class Scheduler {

    private:
        int start_step;
        int stop_step;

        double start_value;
        double stop_value;

        // private methods

        // get step normalized in 0_1 range
        double get_perc_step(int step){

            // remember to cast everything to double!
            double perc_step = static_cast<double>(step - start_step) / static_cast<double>(stop_step - start_step);
            return std::max(0.0, std::min(1.0, perc_step));
        }

        // get value at perc_step
        double get_value(double perc_step){

            return start_value + (stop_value - start_value) * perc_step;
        }

        // virtual (abstract) method
        virtual double warp_func(double perc_step) = 0;

    public:

        // constructor method
        Scheduler(int start_step, int stop_step, double start_value, double stop_value)
            : start_step(start_step), stop_step(stop_step), start_value(start_value), stop_value(stop_value) {

            if (start_step >= stop_step) {
                throw std::invalid_argument("In the scheduler, start step must be less than stop step!");
            }

            if (start_value < stop_value) {
                std::cout << "Initializing Scheduler: ramp from " << start_value << " to " << stop_value << std::endl;
            } else if (start_value > stop_value) {
                std::cout << "Initializing Scheduler: decay from " << start_value << " to " << stop_value << std::endl;
            } else {
                std::cout << "Initializing Scheduler with no effect!" << std::endl;
            }

        }

        // step method to perform the scheduling (used by every child)
        double step(int step){

            // get perc_step normalized into 0_1 range
            double perc_step = get_perc_step(step);

            // warp according to scheduler
            perc_step = warp_func(perc_step);

            // get and return correct value
            return get_value(perc_step);
        }

};


// Linear Scheduler
class LinearScheduler : public Scheduler {

    private:
        double warp_func(double perc_step) override {
            // Linear --> Identity
            return perc_step;
        }

    public:
        // constructor
        LinearScheduler(int start_step, int stop_step, double start_value, double stop_value)
            : Scheduler(start_step, stop_step, start_value, stop_value){
        }
};


// Cosine Scheduler
class CosineScheduler : public Scheduler {

    private:
        double warp_func(double perc_step) override {
            // warp with cosine
            // cos(PI * perc_step) goes from 1 to -1
            // sum 1 and mul 0.5 to normalize
            // then reverse since you still want a perc step as output
            return 1.0 - (0.5 * (1.0 + std::cos(M_PI * perc_step)));
        }

    public:
        // constructor
        CosineScheduler(int start_step, int stop_step, double start_value, double stop_value)
            : Scheduler(start_step, stop_step, start_value, stop_value){
        }
};


// Linear Cosine (start with linear warmup and then cosine)
class LinearCosineScheduler {
private:
    int start_step;
    int stop_step;
    double start_value;
    double stop_value;
    int th_step;
    LinearScheduler linear_wu;
    CosineScheduler cosine_decay;

public:
    // Constructor
    LinearCosineScheduler(int start_step, int stop_step, double start_value, double stop_value, int th_step)
        : start_step(start_step), stop_step(stop_step), start_value(start_value), stop_value(stop_value), th_step(th_step),
          linear_wu(start_step, th_step, 0.0, start_value), cosine_decay(th_step, stop_step, start_value, stop_value) {
        if (start_value <= stop_value) {
            throw std::invalid_argument("The LinearCosine Scheduler must decay.");
        }

        if (!(start_step < th_step && th_step < stop_step)) {
            throw std::invalid_argument("In the scheduler, threshold step must lie between start and stop steps!");
        }
    }

    // Step method
    double step(int step) {
        if (step < th_step) {
            return linear_wu.step(step);
        } else {
            return cosine_decay.step(step);
        }
    }
};


// example main
int main() {
    // Define the parameters for the LinearCosineScheduler
    int start_step = 0;
    int stop_step = 100;
    double start_value = 0.1;
    double stop_value = 0.001;
    int th_step = 50;

    // Create an instance of the LinearCosineScheduler
    LinearCosineScheduler scheduler(start_step, stop_step, start_value, stop_value, th_step);

    // Test the scheduler by printing values at different steps
    for (int step = 0; step <= stop_step; ++step) {
        double value = scheduler.step(step);
        std::cout << "Step " << step << ": Learning rate = " << value << std::endl;
    }

    return 0;
}


// ctypes Bindings
extern "C" {

    // Linear Scheduler
    void* LinearScheduler_create(int start_step, int stop_step, double start_value, double stop_value) {
        return new LinearScheduler(start_step, stop_step, start_value, stop_value);
    }

    double LinearScheduler_step(void* instance, int step) {
        return static_cast<LinearScheduler*>(instance)->step(step);
    }

    void LinearScheduler_destroy(void* instance) {
        delete static_cast<LinearScheduler*>(instance);
    }

    // Cosine Scheduler
    void* CosineScheduler_create(int start_step, int stop_step, double start_value, double stop_value) {
        return new CosineScheduler(start_step, stop_step, start_value, stop_value);
    }

    double CosineScheduler_step(void* instance, int step) {
        return static_cast<CosineScheduler*>(instance)->step(step);
    }

    void CosineScheduler_destroy(void* instance) {
        delete static_cast<CosineScheduler*>(instance);
    }

    // LinearCosine Scheduler
    void* LinearCosineScheduler_create(int start_step, int stop_step, double start_value, double stop_value, int th_step) {
        return new LinearCosineScheduler(start_step, stop_step, start_value, stop_value, th_step);
    }

    double LinearCosineScheduler_step(void* instance, int step) {
        return static_cast<LinearCosineScheduler*>(instance)->step(step);
    }

    void LinearCosineScheduler_destroy(void* instance) {
        delete static_cast<LinearCosineScheduler*>(instance);
    }
}
