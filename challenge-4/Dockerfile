# Dockerfile
# docker build -t chall4 .
# docker run -d --name chall4 -p 8080:8080 chall4:latest
# docker exec -it -u ctfuser chall4 /bin/sh
FROM node:20-alpine

# Create unprivileged interactive user
RUN adduser -D ctfuser

WORKDIR /app
COPY server.js .

EXPOSE 8080

ENV FLAG=Bunian{fake_but_not_actually_because_we_dont_have_remote}

CMD ["node", "server.js"]

