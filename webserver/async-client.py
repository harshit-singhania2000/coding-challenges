import asyncio
import time
async def client(message):
    start = time.time()
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.readuntil(b";")
    print(f'Received: {data.decode()!r}')

    print('Close the connection. latency:', time.time()-start)
    writer.close()
    await writer.wait_closed()

async def main():
    MESSAGE = "abcd%s;"
    await asyncio.gather(*[client(MESSAGE%i) for i in range(2000)])

asyncio.run(main())