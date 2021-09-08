import asyncio
import httpx
import time
import threading

semaphore = threading.BoundedSemaphore(value=15)

async def main(i: int):
    semaphore.acquire()
    try:
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{i}'

        async with httpx.AsyncClient() as client:

            resp = await client.get(pokemon_url)

            pokemon = resp.json()
            pokemon_name = pokemon['name']
            #pokemon_type = pokemon['types']['type']['name']
            print(f'{i} {pokemon_name}')
    except Exception as err:
        print(f'For iteration {i}, {err=}')
    semaphore.release()

if __name__ == "__main__":
    start_time = time.perf_counter()
    thread_list = []
    #for i in range(100):
    #    asyncio.run(main(i))
    for i in range(1,1118):
        t = threading.Thread(target=asyncio.run, args=(main(i),))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f'Total duration: {duration:.2f} seconds, count {len(thread_list)}')