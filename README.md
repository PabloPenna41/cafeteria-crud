# Gestão da Cafeteria (CRUD PHP + Tkinter)

CRUD completo de cardápio. Backend em **PHP procedural + MySQLi (prepared statements)** e front em **Python/Tkinter**.

## Estrutura
- `banco.sql`: script do banco (importar no phpMyAdmin).
- `php/`: `login.php`, `logout.php`, `painel.php` (listar/cadastrar), `editar_item.php`, `excluir_item.php`.
- `app.py`: front em Tkinter.
- `windows/CafeteriaApp.exe`: executável para Windows (gerado automaticamente pelo GitHub Actions).
- `run.sh`: atalho para Linux (sobe banco + PHP + app).

## Windows (XAMPP)
1. Instale o [XAMPP](https://www.apachefriends.org/) e inicie **Apache** e **MySQL**.
2. No phpMyAdmin, execute o `banco.sql`.
3. Copie a pasta `php` para `C:\xampp\htdocs\cafeteria\php`.
4. Execute `windows/CafeteriaApp.exe` (mantenha o `servidor.txt` ao lado dele; se o endereço for outro, edite-o).
5. Login: `admin` / `admin123`.

## Rodando o Python direto
```
pip install requests
python app.py
```
