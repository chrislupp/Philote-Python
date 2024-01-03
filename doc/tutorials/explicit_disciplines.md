(tutorials:explicit)=
# Working with Explicit Disciplines



## Disciplines

Before we take a closer look at clients and servers, we need a discipline that
we will attach to a server and call from the client. Philote-Python implements
disciplines in a similar way to OpenMDAO. We create a class, inheriting from a
base class and then specialize some methods to run the calculations we want.

To illustrate this, let us take a look at a simple paraboloid problem (the same
problem as in the OpenMDAO documentation):

\begin{align}
f(x,y) &= (x-3)^2 + x y + (y+4)^2 - 3
\end{align}


## Setup Functions

To create a discipline that executes this equation, we create a class and
inherit from the ExplicitDiscipline class Philote-Python provides. First, let us
look at the setup member function:

:::{code-block} python
import philote.general as pm

class Paraboloid(pmdo.ExplicitDiscipline):

    def setup(self):
        self.add_input("x", shape=(1,), units="m")
        self.add_input("y", shape=(1,), units="m")

        self.add_output("f_xy", shape=(1,), units="m**2")
:::

The **setup** function exists to define the inputs and outputs of a discipline
(this purpose is borrowed from the OpenMDAO workflow, which operates the same
way). The **add_input** and **add_output** member functions are provided by the
**ExplicitDiscipline** to define both inputs and outputs. Here, two inputs (*x*
and *y*) are defined, each with the shape of 1 (scalar) and with a unit of
meters (no physical meaning, purely for demonstration). Furthermore, a scalar
output (*f_xy*) was defined with the units of square meters.

While the discipline gradients (or partials) can be defined within the **setup**
function, it usually is good practice to separate these definitions into the
**setup_partials** functions. Behind the scenes, both functions (setup and
setup_partials) are called back-to-back, so there is no actual difference where
the gradients are defined. However, using both functions to define the variables
and partials may have organizational benefits. To define the gradient of an
output with respect to an input, the **declare_partials** function is invoked:

:::{code-block} python
    def setup_partials(self):
        self.declare_partials("f_xy", "x")
        self.declare_partials("f_xy", "y")
:::


## Compute Function

To implement the paraboloid function, the **compute** member function must be
defined:

:::{code-block} python
    def compute(self, inputs, outputs):
        x = inputs["x"]
        y = inputs["y"]

        outputs["f_xy"] = (x - 3.0) ** 2 + x * y + (y + 4.0) ** 2 - 3.0
:::

The *inputs* and *outputs* variables for this function are later passed in by
the server as dictionaries with the variable names as the keys.


## Gradient Function

To implement the paraboloid function, the **compute** member function must be
defined:

:::{code-block} python
    def compute(self, inputs, outputs):
        x = inputs["x"]
        y = inputs["y"]

        outputs["f_xy"] = (x - 3.0) ** 2 + x * y + (y + 4.0) ** 2 - 3.0
:::

The *inputs* and *outputs* variables for this function are later passed in by
the server as dictionaries with the variable names as the keys.


## Summary


## API Reference