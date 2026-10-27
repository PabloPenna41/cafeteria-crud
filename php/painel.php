<?php
require 'config.php';
exigir_login();

// C - Create
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome = trim($_POST['nome_item'] ?? '');
    $categoria = trim($_POST['categoria'] ?? '');
    $descricao = trim($_POST['descricao'] ?? '');
    $preco = str_replace(',', '.', $_POST['preco'] ?? '');

    if ($nome === '' || $categoria === '' || !is_numeric($preco) || $preco < 0) {
        responder(['ok' => false, 'erro' => 'Dados inválidos'], 400);
    }
    $preco = (float)$preco;

    $stmt = mysqli_prepare($conn, "INSERT INTO cardapio (nome_item, categoria, descricao, preco) VALUES (?, ?, ?, ?)");
    mysqli_stmt_bind_param($stmt, 'sssd', $nome, $categoria, $descricao, $preco);
    if (!mysqli_stmt_execute($stmt)) {
        responder(['ok' => false, 'erro' => 'Erro ao cadastrar'], 500);
    }
    responder(['ok' => true, 'id' => mysqli_insert_id($conn)]);
}

// R - Read
$res = mysqli_query($conn, "SELECT id, nome_item, categoria, descricao, preco FROM cardapio ORDER BY id DESC");
$itens = [];
while ($linha = mysqli_fetch_assoc($res)) {
    $itens[] = $linha;
}
responder(['ok' => true, 'usuario' => $_SESSION['usuario_nome'], 'itens' => $itens]);
