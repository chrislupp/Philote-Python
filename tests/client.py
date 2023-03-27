from philote_mdo.general import ExplicitClient


client = ExplicitClient()
client.host = 'localhost:50051'

client._setup_connection()
client._stream_options()
client._setup()
