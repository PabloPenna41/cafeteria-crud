<?php
require 'config.php';
exigir_login();

$id = (int)($_GET['id'] ?? 0);
if ($id <= 0) {
    responder(['ok' => false, 'erro' => 'ID inválido'], 400);
}

// U - Update
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome = trim($_POST['nome_item'] ?? '');
    $categoria = trim($_POST['categoria'] ?? '');
    $descricao = trim($_POST['descricao'] ?? '');
    $preco = str_replace(',', '.', $_POST['preco'] ?? '');

    if ($nome === '' || $categoria === '' || !is_numeric($preco) || $preco < 0) {
        responder(['ok' => false, 'erro' => 'Dados inválidos'], 400);
    }
    $preco = (float)$preco;

    $stmt = mysqli_prepare($conn, "UPDATE cardapio SET nome_item = ?, categoria = ?, descricao = ?, preco = ? WHERE id = ?");
    mysqli_stmt_bind_param($stmt, 'sssdi', $nome, $categoria, $descricao, $preco, $id);
    if (!mysqli_stmt_execute($stmt)) {
        responder(['ok' => false, 'erro' => 'Erro ao atualizar'], 500);
    }
    responder(['ok' => true]);
}

// GET: dados atuais para preencher o formulário
$stmt = mysqli_prepare($conn, "SELECT id, nome_item, categoria, descricao, preco FROM cardapio WHERE id = ?");
mysqli_stmt_bind_param($stmt, 'i', $id);
mysqli_stmt_execute($stmt);
$item = mysqli_fetch_assoc(mysqli_stmt_get_result($stmt));
if (!$item) {
    responder(['ok' => false, 'erro' => 'Item não encontrado'], 404);
}
responder(['ok' => true, 'item' => $item]);
