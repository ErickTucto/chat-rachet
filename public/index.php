<?php

use Bramus\Router\Router;
use Twig\Environment;
use Twig\Loader\FilesystemLoader;
use Whoops\Handler\PrettyPageHandler;
use Whoops\Run;

require __DIR__ . '/../vendor/autoload.php';

$whoops = new Run();
$whoops->pushHandler(new PrettyPageHandler);
$whoops->register();

function view(string $path, array $data = []) {
    $loader = new FilesystemLoader(__DIR__ . '/../views');
    $twig = new Environment($loader, [
        //'cache' => __DIR__ . '/../storage/cache/views',
    ]);
    $template = $twig->load($path);
    return $template->render($data);
}

$router = new Router();

$router->get("/", function () {
    echo view("index.twig");
});

$router->run();
