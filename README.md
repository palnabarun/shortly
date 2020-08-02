# Shortly

> Note: This is a teaching effort and not supposed to be used in production at its current state

## Targets

Build a simple URL shortener

Input: URL -> Ouput: Reference to it

## Requirements from a hashing algorithm

1. The generated hash should be small
2. The hashes should be unique
3. The hashes should have one to one mapping with the url

## API

## Milestone 1

### Creating a short url

    POST /api

    {
        "url": "https://dgplug.org"
    }

    200 OK

    {
        "url": "https://dgplug.org"
        "short_url": "abcd"
    }


### Accessing the shortened URL

    GET /abcd

    301 Moved Permananently
    Location: https://dgplug.org


## Milestone 2

- Server should persist url_map to a db

### Creating a short url

    POST /api

    {
        "url": "https://dgplug.org",
        "short_url": "hey-dgplug",
        "strict": true
    }

    200 OK

    {
        "url": "https://dgplug.org",
        "short_url": "hey-dgplug"
    }
    ---
    409 Conflict
    {
        "error": "hey-dgplug already exists. Set strict=false for getting a random id appended."
    }

### Accessing the shortened URL

    GET /abcd

    301 Moved Permananently
    Location: https://dgplug.org

## IDEAS

Whenever request comes,
1. Block 1 precomputed key
2. add that key to your url map
3. send response for user


    HASH    | USED
    a       | True
    b       | False


    HASH    | URL           | EXPIRY    | USER_ID
    a       | dgplug.org    | null      | 1
