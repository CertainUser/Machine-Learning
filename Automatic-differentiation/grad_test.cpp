#include <iostream>
#include <unordered_map>
#include <initializer_list>

typedef std::unordered_map<std::string, double> d_map;

bool alreadyIncluded(const d_map& map, std::string element) {
    auto it = map.find(element);
    return it != map.end();
}

int counter = 0;

int updateCounter() {
    ++counter;
    return counter;
}

std::string getNewName() {
    return "v_" + std::to_string(updateCounter());
}

class Variable {
public:
    Variable(): name("c"), value(0.0), grad(), isConstant(true) {}
    Variable(const double& value):  name("c"), value(value), grad(), isConstant(true) {}
    Variable(const double& value, std::string name): name(name), value(value), grad(), isConstant(false) {}
    Variable(const double& value, const d_map& derivatives): name("c"), value(value), grad(derivatives), isConstant(true) {}
    Variable(const double& value, std::string name, const d_map& derivatives): name(name), value(value), grad(derivatives), isConstant(false) {}


    friend std::string getNewName();

    friend std::ostream& operator<<(std::ostream& os, const Variable& variable);
    
    friend Variable add(std::initializer_list<Variable> init);


    // Operator overloading currently works if only one operation is performed in a line of code because each call creates a new variable
    Variable operator+(const Variable& other) {
        d_map new_grad = d_map();

        if (this->name == other.name) {
            for (const auto& [df, value]: this->grad) {
                this->grad[df] *= 2; 
            }        

            return Variable(2 * this->value, getNewName(), new_grad);
        }

        double new_value = this->value += other.value;
        new_grad[this->name] = 1.0;
        new_grad[other.name] = 1.0;


        for (const auto& [df, value]: this->grad) {
            new_grad[df] += 1; 
        }        

        // Iterate through the derivatives of the 'other' variable
        for (const auto& [df, value]: other.grad) {
            new_grad[df] += value; 
        }        

        return Variable(new_value, getNewName(), new_grad);
    }

    Variable operator+(const double& constant) {
        double new_value = this->value + constant;
        d_map new_grad = this->grad;
        new_grad[this->name] = 1.0;
        return Variable(new_value, getNewName(), new_grad);
    }

    // Creates a new variable
    Variable operator-() {
        double new_value = -this->value;
        if (isConstant) return Variable(new_value);

        d_map new_grad = this->grad;

        for (const auto& [name, derivative]: new_grad) {
            new_grad[name] *= -1;
        }
        new_grad[this->name] = -1;
        return Variable(new_value, getNewName(), new_grad);
    }

    void Grad() {
        for (const auto& [withRespectTo, derivative]: this->grad) {
            printf("d%s/d%s = %g\n", this->name.c_str(), withRespectTo.c_str(), derivative);
        }
        std::cout << '\n';
    }

    const d_map getDerivatives() const { return this->grad; }

    std::string name;
    d_map grad;
    double value;
    bool isConstant;
};


std::ostream& operator<<(std::ostream& os, const Variable& variable) {
    os << variable.value;
    return os;
}

Variable add(std::initializer_list<Variable> init) {
        double new_value = 0;
        d_map new_grad = d_map();

        for (const Variable& variable: init) {
            new_value += variable.value;
            
            if (!variable.isConstant)
                new_grad[variable.name] += 1.0;


            for (const auto& [df, value]: variable.grad) {
                new_grad[df] += value;
            }        
        }
        return Variable(new_value, getNewName(), new_grad);
}

namespace diff {
    Variable Constant(double value) {
        return Variable(value);
    }
}

int main() {
    Variable x = Variable(5, "x");
    Variable y = Variable(7, "y");
    auto a = diff::Constant(16.5);

    Variable v_1 = y + x;
    Variable v_2 = add({v_1, x, a});
    v_1.Grad();
    v_2.Grad();

    return 0;
}
