from fastapi import FastAPI
from azure.eventhub import EventHubProducerClient, EventData

app = FastAPI()

# Substitua com a sua própria URL de conexão
connection_str = "Endpoint=sb://estudostream.servicebus.windows.net/;SharedAccessKeyName=testeEvtEstudo;SharedAccessKey=Bwn/qhR5a7esnGg6AElCpA5Oqhv9VXho2+AEhENvRjI=;EntityPath=dadosestudo"
eventhub_name = "dadosestudo"
#connection_str = "Endpoint=sb://evthubura.servicebus.windows.net/;SharedAccessKeyName=PolAnlUraBaseUnica;SharedAccessKey=zqKyinnR4MtO3I/nAxnOjyD5ftOprr62m+AEhGl/09k=;EntityPath=evthuvurabaseunica"
#eventhub_name = "evthuvurabaseunica"


@app.post("/enviar-dados")
async def enviar_dados(dados: dict):
    try:
        if isinstance(dados['clienteEncontrado'], bool):
            if dados['clienteEncontrado'] == True:
                dados['clienteEncontrado'] = 'True'
            else:
                dados['clienteEncontrado'] = 'False'
        
        producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)
        
        with producer:
            event_data_batch = producer.create_batch()

            # Adicione os dados que deseja enviar ao lote
            event_data_batch.add(EventData(str(dados)))

            producer.send_batch(event_data_batch)
            return dados
    except Exception as e:
        return {"erro": str(e)}
'''if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)'''
