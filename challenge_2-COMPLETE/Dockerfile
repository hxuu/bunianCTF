FROM python:3.13-alpine3.19

# Install dependencies
RUN apk update && apk add --no-cache socat bash coreutils

# Create hxuu user and home
RUN adduser -D -h /home/hxuu -s /bin/bash hxuu

# Copy challenge script
COPY jail.py /home/hxuu/jail.py

# You can't guess the flag name :)
RUN FLAG_NAME="flag-$(head -c16 /dev/urandom | od -An -tx1 | tr -d ' \n').txt" \
    && echo "flag{y0u_e5caped_7h3_J41l_$(head -c5 /dev/urandom | od -An -tx1 | tr -d ' \n')}" > "/home/hxuu/${FLAG_NAME}" \
    && chmod 444 "/home/hxuu/${FLAG_NAME}"

# Switch to hxuu user
USER hxuu
WORKDIR /home/hxuu

# Run hxuuenge service
ENTRYPOINT ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:\"python /home/hxuu/jail.py\""]

