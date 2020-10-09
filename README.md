# Timpview CS Club Week 2
## Machine Learning

----

# Setup
## Step 1.
Download or clone this repository. If you have `git` run the command

    git clone https://github.com/programjames/timpviewcsclubweek2.git

Otherwise you can click the button that says "↓ Code!" and then "Download ZIP".

## Step 2.
Install dependencies. Do you have Python on your computer yet? If not, download
it here: https://www.python.org/downloads/release/python-379/

Now, go to the command line and run the following commands:

    pip install numpy
    pip install matplotlib

If `pip` isn't working, troubleshoot on Google.

----

# Examples

I've included two examples in this repository. One is a genetic algorithm
that finds an approximation to `e` (about 2.718) using only the digits 1 through
9 and the operators `+ - * / ^`. Note: it writes the expression in Reverse
Polish Notation because it simplifies the coding.

The second example creates a neural net that approximates the xor operator. The
xor operator works as follows:

    0 ⊕ 0 = 0
    1 ⊕ 0 = 1
    0 ⊕ 1 = 1
    1 ⊕ 1 = 0

So, if you feed into the neural net the values `[0, 1]` you would expect it to
return `1`. The example trains a neural net to get the right outputs for these
given inputs.

----

# Problems
There are two problems for you to solve. The neural net one is easier, but the
genetic algorithm one is cooler :)

## Neural Net Problem (TicTacToe Analyzer)

In this problem you need to train a neural net to be able to identify the winner
in a game of TicTacToe. I've included a function to test your code. To see more
on the details of the problem, read the comments in the actual file.

**Hint:** Try generating 100 random boards and training your neural net on those
like I did with the xor function. What if you generated every possible
TicTacToe board and then trained the neural net on that?

## Genetic Algorithm Problem (Land a Rocket!)

In this problem you control a rocket and need to bring it safely to the ground.
I have included a `Rocket` class in addition with a `draw` function to help you
in your simulations. To see more on the details of the problem, read the
comments in the actual file.

**Hint:** You don't actually need any of the intermediate inputs. You can just
predetermine what angles and power your rocket will take each turn (make this
your genome).

*Extra fun* (not necessary for this problem): Try combining using a genetic
algorithm with a neural net. So, the weights and biases in your neural net could
be the genome for the genetic algorithm. Use the turn-by-turn inputs + all of
the starting inputs as the inputs into the neural net.
