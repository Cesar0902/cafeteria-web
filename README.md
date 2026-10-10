# Café Aurora

Página de presentación adaptable en español de una cafetería ficticia para
la actividad académica Tarea 3. Utiliza HTML y CSS, fuentes del sistema e
ilustraciones creadas con CSS: sin compilación, JavaScript, recursos externos
ni dependencias. No es una cafetería real y no ofrece compras, reservas,
visitas ni información de una ubicación real.

## Vista previa local

Desde la raíz del repositorio, con Python 3 instalado, ejecuta:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Abre `http://127.0.0.1:8000/`. Detén el servidor con `Ctrl+C`.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
git diff --check
```

Las pruebas verifican el idioma del documento, los metadatos, los nombres
accesibles, textos representativos, la estructura, los enlaces internos,
el aviso académico y las reglas CSS de adaptación y foco del teclado.
No sustituyen la revisión en un navegador del diseño, el contraste y la
navegación con teclado. Comprueba también la página en anchos de móvil y escritorio.

## Alojamiento estático

Publica `index.html` y `styles.css` juntos, en el mismo directorio, en un
servicio de alojamiento estático. No se necesita un comando de compilación;
la carpeta de publicación debe contener ambos archivos. La configuración del
servicio y sus credenciales quedan a cargo de quien publica el sitio.
No incluyas `.atl/` ni `tests/__pycache__/` en la publicación.

Después de publicar, verifica que la página y la hoja de estilos carguen
correctamente y revisa los enlaces, el diseño y el teclado en un navegador.
Estas son instrucciones de publicación, no una confirmación de despliegue.
