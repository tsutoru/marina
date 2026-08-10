FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ocaml opam make git python3 \
    && opam init --disable-sandboxing -y \
    && opam install -y ocamlfind ounit2

WORKDIR /app
COPY . .

RUN eval $(opam env) && make

COPY server.py .

ENV PORT=8080
CMD ["python3", "server.py"]