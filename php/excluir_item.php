<?php
require 'config.php';
exigir_login();

// D - Delete (id via URL: ?id=X)
$id = (int)($_GET['id'] ?? 0);
if ($id <= 0) {
    responder(['ok' => false, 'erro' => 'ID inválido'], 400);
}

$stmt = mysqli_prepare($conn, "DELETE FROM cardapio WHERE id = ?");
mysqli_stmt_bind_param($stmt, 'i', $id);
mysqli_stmt_execute($stmt);

if (mysqli_stmt_affected_rows($stmt) > 0) {
    responder(['ok' => true]);
}
responder(['ok' => false, 'erro' => 'Item não encontrado'], 404);
