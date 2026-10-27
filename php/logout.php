<?php
require 'config.php';
session_destroy();
responder(['ok' => true]);
