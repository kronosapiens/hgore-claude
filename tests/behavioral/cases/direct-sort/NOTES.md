# Optional recovery idea

Someone proposed a durable operation log in case a concurrent runtime patch replaces the sorting function, memory corruption damages the input, and the process is killed during the same call.
There are no incidents, reproductions, or supported workflows establishing this scenario.
No additional recovery behavior was requested.
