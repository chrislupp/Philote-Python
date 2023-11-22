(tutorials:explicit)=
# Working with Explicit Disciplines

While the discipline gradients (or partials) can be defined within the **setup**
function, it usually is good practice to separate these definitions into the
**setup_partials** functions. Behind the scenes, both functions (setup and
setup_partials) are called back-to-back, so there is no actual difference where
the gradients are defined. To define the gradient of an output with respect to
an input, the **declare_partials** function is invoked:

:::{code-block} python
    def setup_partials(self):
        self.declare_partials("f_xy", "x")
        self.declare_partials("f_xy", "y")
:::