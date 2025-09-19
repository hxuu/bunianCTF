## BunianCTF 4th Challenge

### Description

Can you read the flag from the webserver?

### How to run the code

```bash
# make sure you're inside this directory
docker build -t chall4 .
docker run -d --name chall4 -p 8080:8080 chall4:latest
docker exec -it -u ctfuser chall4 /bin/sh
```

> [!TIP]
> You can interact with the challenge on `http://localhost:8080`

Solutions by just catting out /proc/<pid>/environ don't count :)

---

Do share your screenshot of the solve ;)

