import numpy as np
from philote_mdo.general import ExplicitClient


client = ExplicitClient()
client.host = 'localhost:50051'

# connect to the server
client._setup_connection()

# transfer the stream options to the server
client._stream_options()

# run setup
client._setup()

# define some inputs
inputs = {
    "x": np.array([1.0]),
    "y": np.array([2.0])
}
outputs = {}

client._compute(inputs, outputs)

print(outputs)
