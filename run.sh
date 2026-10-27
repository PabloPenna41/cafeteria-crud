#!/usr/bin/env bash
# Sobe MariaDB + servidor PHP + app Tkinter. Uso: ./run.sh
DIR="$(cd "$(dirname "$0")" && pwd)"
DBDIR="$HOME/cafe-db"
MARIA="$DBDIR/mariadb-11.4.5-linux-systemd-x86_64"
export LD_LIBRARY_PATH="$DBDIR/lib"

cleanup() {
  echo "Encerrando..."
  [ -n "$PHP_PID" ] && kill "$PHP_PID" 2>/dev/null
  [ -n "$DB_PID" ] && kill "$DB_PID" 2>/dev/null
}
trap cleanup EXIT

# 1) Banco
if ! "$MARIA/bin/mariadb" --no-defaults -uroot -h127.0.0.1 -e "select 1" >/dev/null 2>&1; then
  setsid "$MARIA/bin/mariadbd" --no-defaults --basedir="$MARIA" --datadir="$DBDIR/data" \
    --socket="$DBDIR/my.sock" --port=3306 --bind-address=127.0.0.1 >"$DBDIR/log.txt" 2>&1 &
  DB_PID=$!
  for i in $(seq 1 30); do
    "$MARIA/bin/mariadb" --no-defaults -uroot -h127.0.0.1 -e "select 1" >/dev/null 2>&1 && break
    sleep 1
  done
fi
"$MARIA/bin/mariadb" --no-defaults -uroot -h127.0.0.1 -e "use gestao_cafeteria" >/dev/null 2>&1 \
  || "$MARIA/bin/mariadb" --no-defaults -uroot -h127.0.0.1 < "$DIR/banco.sql"

# 2) Servidor PHP
DB_HOST=127.0.0.1 php -d extension=mysqli -S 127.0.0.1:8080 -t "$(dirname "$DIR")" >"$DBDIR/php.log" 2>&1 &
PHP_PID=$!
sleep 1

# 3) App
CAFETERIA_URL=http://127.0.0.1:8080/cafeteria/php python3 "$DIR/app.py"
