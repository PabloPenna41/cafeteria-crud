<?php
session_start();
header('Content-Type: application/json; charset=utf-8');

$conn = mysqli_connect(getenv('DB_HOST') ?: 'localhost', 'root', '', 'gestao_cafeteria');
if (!$conn) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'erro' => 'Falha na conexão com o banco']);
    exit;
}
mysqli_set_charset($conn, 'utf8mb4');

function responder($dados, $codigo = 200) {
    http_response_code($codigo);
    echo json_encode($dados, JSON_UNESCAPED_UNICODE);
    exit;
}

function exigir_login() {
    if (!isset($_SESSION['usuario_id'])) {
        responder(['ok' => false, 'erro' => 'Não autenticado'], 401);
    }
}
