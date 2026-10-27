<?php
require 'config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    responder(['ok' => false, 'erro' => 'Use POST'], 405);
}

$usuario = trim($_POST['usuario'] ?? '');
$senha = $_POST['senha'] ?? '';

$stmt = mysqli_prepare($conn, "SELECT id, nome, senha FROM usuarios WHERE usuario = ?");
mysqli_stmt_bind_param($stmt, 's', $usuario);
mysqli_stmt_execute($stmt);
mysqli_stmt_bind_result($stmt, $id, $nome, $hash);

if (mysqli_stmt_fetch($stmt)) {
    // Aceita senha em texto puro (script da aula) ou hash gerado por password_hash
    if ($senha === $hash || password_verify($senha, $hash)) {
        $_SESSION['usuario_id'] = $id;
        $_SESSION['usuario_nome'] = $nome;
        responder(['ok' => true, 'nome' => $nome]);
    }
}
responder(['ok' => false, 'erro' => 'Usuário ou senha inválidos'], 401);
