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

## Milestone 3

- Add a length parameter to the user request. Have a sane minimum (5) and maximum (15).
- Server should persist url_map to a db

## IDEAS

Whenever request comes,
1. Block 1 precomputed key
2. add that key to your url map
3. send response for user

```
    HASH    | USED
    a       | True
    b       | False


    HASH    | URL           | EXPIRY    | USER_ID
    a       | dgplug.org    | null      | 1
```

Truth table for the short url and strictness check logic:

```
short_url | strict | short_url is present   |
"foo"     | true   | true                   | 409 CHECK
"foo"     | true   | false                  | "foo" CHECK
"foo"     | false  | true                   | "foo-random" CHECK
"foo"     | false  | false                  | "foo" CHECK
""        | true   | true                   | "random"
""        | true   | false                  | "random"
""        | false  | true                   | "random"
""        | false  | false                  | "random"
```
