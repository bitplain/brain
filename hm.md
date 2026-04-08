# Аудит рабочего каталога `brain`

Дата осмотра: 2026-04-08  
Формат: иерархический аудит текущего состояния на диске, включая служебные и временные артефакты.

## Краткая картина

- Репозиторий: `bitplain/brain`
- Удалённый origin: `https://github.com/bitplain/brain`
- Текущая ветка: `main`
- Последние коммиты:
  - `f1e9453` `Merge pull request #1 from bitplain/copilot/initialize-project-with-description`
  - `e08d278` `docs: add init.md with project description`
  - `d58f5e5` `Initial Zensical docs setup`
- Общий характер проекта: небольшой репозиторий документации на Zensical с локальным bootstrap-скриптом для скачивания wheel-артефакта и задачами VS Code для preview/build.
- Найдено в рабочем каталоге:
  - исходники документации в `docs/`
  - конфигурация Zensical в `zensical.toml`
  - локальный Python-скрипт запуска в `scripts/zensical_cli.py`
  - служебные каталоги `.git/`, `.venv/`, `.tools/`, `.vscode/`
  - временный файл `wget-log`

## Git-состояние

- Рабочее дерево не чистое.
- `D .github/workflows/docs.yml`
  - Отслеживаемый workflow удалён из рабочего дерева.
  - В `HEAD` это был workflow деплоя документации на GitHub Pages.
  - Он делал `actions/configure-pages`, `actions/checkout`, `actions/setup-python`, затем `pip install zensical`, `zensical build --clean`, `upload-pages-artifact`, `deploy-pages`.
- `M .gitignore`
  - Добавлены игнорируемые пути `.tools/zensical/` и `.tools/zensical-test/`.
- `M docs/init.md`
  - Добавлен раздел про запуск из VS Code, bootstrap, preview, build, автопроброс порта `8000`, локальный кэш `.tools/zensical` и остановку preview-задачи.
- `?? .vscode/`
  - Добавлены локальные конфиги редактора.
- `?? scripts/`
  - Добавлен локальный bootstrap/run-скрипт для Zensical.
- `?? wget-log`
  - Временный лог сетевой загрузки.
- `git diff --stat`:
  - удалён 1 workflow-файл на 29 строк
  - добавлено 23 строки в двух файлах

## Дерево проекта

### Корень

- `zensical.toml`
  - Основной конфиг Zensical.
  - `site_name = "Documentation"`, `site_description = "A new project generated from the default template project."`, `site_author = "<your name here>"`.
  - Явный `site_url` не задан.
  - Навигация `nav` закомментирована, значит структура страниц в основном выводится из `docs/`.
  - Включены функции темы и контента:
    - `announce.dismiss`
    - `content.code.annotate`
    - `content.code.copy`
    - `content.code.select`
    - `content.footnote.tooltips`
    - `content.tabs.link`
    - `content.tooltips`
    - `navigation.footer`
    - `navigation.indexes`
    - `navigation.instant`
    - `navigation.instant.prefetch`
    - `navigation.path`
    - `navigation.sections`
    - `navigation.top`
    - `navigation.tracking`
    - `search.highlight`
  - Язык интерфейса: `en`.
  - Палитры две: `default` и `slate`, с переключением светлой/тёмной темы.
  - Дополнительные CSS/JS, logo, social links и часть настроек темы пока закомментированы, то есть проект во многом шаблонный.
- `.gitignore`
  - Игнорируются `.venv/`, `site/`, `__pycache__/`, `*.pyc`, `.tools/zensical/`, `.tools/zensical-test/`.
- `wget-log`
  - Лог `wget`, не относящийся напрямую к проекту.
  - Показывает попытку загрузить большой VSIX-пакет `openai/chatgpt` из `openai.gallerycdn.vsassets.io`.
  - Размер файла по логу: около `377M`.
  - Загрузка шла в `/tmp/openai.chatgpt.wget.vsix`.
  - Была ошибка `Read error at byte 1093/395098612 (Connection timed out)`, после чего началась повторная попытка с `206 Partial Content`.
  - Это побочный артефакт среды, а не часть функционала репозитория.
- `hm.md`
  - Этот файл-аудит, созданный по запросу.

### `docs/`

- Назначение каталога: исходные Markdown-страницы документационного сайта.
- Объём каталога: небольшой, три основных страницы.
- `docs/index.md`
  - Шаблонная стартовая страница Zensical.
  - Содержит демонстрации возможностей: admonitions, details, code blocks, content tabs, mermaid, footnotes, formatting, emojis, math, task lists, tooltips.
  - Присутствует inline-подключение MathJax через `unpkg.com`.
  - По смыслу это стартовый пример, а не кастомное описание проекта `brain`.
- `docs/init.md`
  - Русскоязычное описание проекта `Brain`.
  - Позиционирует репозиторий как базу знаний и техническую документацию на Zensical от `bitplain`.
  - Описывает структуру проекта, базовые команды и работу через VS Code.
  - На текущем рабочем дереве расширен блоком про bootstrap, preview, build и проброс порта `8000`.
- `docs/markdown.md`
  - Шпаргалка по Markdown.
  - Покрывает заголовки, форматирование текста, ссылки и изображения, списки, цитаты, code blocks, таблицы, горизонтальные правила, task lists, escaping, line breaks.
  - Содержимое выглядит шаблонным и учебным.

### `scripts/`

- Назначение каталога: локальные скрипты запуска.
- `scripts/zensical_cli.py`
  - Python-обёртка для запуска Zensical без предварительной установки в окружение проекта.
  - Версия Zensical зафиксирована как `0.0.32`.
  - Есть таблица wheel-артефактов для платформ:
    - Linux `x86_64`, `aarch64`
    - macOS `x86_64`, `arm64`
    - Windows `x86_64`
  - Кэш артефактов: `.tools/zensical/0.0.32/`.
  - Скрипт:
    - нормализует платформу и архитектуру
    - при необходимости скачивает wheel из GitHub Releases
    - распаковывает wheel в локальный кэш
    - запускает `python -m zensical` с подмешанным `PYTHONPATH`
  - Поддерживает режим `bootstrap` и проксирование остальных аргументов в Zensical.
  - Практический смысл: репозиторий можно запускать без `pip install zensical`.

### `.vscode/`

- Назначение каталога: локальная интеграция с VS Code.
- `.vscode/tasks.json`
  - Определены три shell-задачи:
    - `Brain: Bootstrap Zensical`
    - `Brain: Preview site`
    - `Brain: Build site`
  - Все задачи используют `python3 scripts/zensical_cli.py ...`.
  - Preview запускается как background-task на `127.0.0.1:8000`.
- `.vscode/launch.json`
  - Есть две конфигурации `node-terminal`:
    - preview сайта
    - build сайта
- `.vscode/settings.json`
  - Включены `remote.autoForwardPorts` и `remote.restoreForwardedPorts`.
  - Для порта `8000` задан label `Brain preview` и поведение `openBrowser`.
  - Это хорошо согласуется с инструкциями из `docs/init.md`.

### `.github/`

- Каталог существует, но в рабочем дереве фактически пуст.
- Подкаталог `.github/workflows/` есть, но файлов в нём сейчас нет.
- По git-истории видно, что ранее там был `docs.yml` для GitHub Pages.
- То есть CI/CD-конфигурация была, но сейчас удалена локальными изменениями.

### `.tools/`

- Назначение каталога: локальный кэш инструментов.
- `.tools/zensical/0.0.32/zensical-0.0.32-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.download`
  - Недокачанный или промежуточный файл загрузки wheel-артефакта Zensical для Linux `x86_64`.
  - Размер в момент осмотра: около `3.6M`.
  - Распакованного `extracted/` рядом не найдено.
  - Это указывает, что bootstrap либо не был завершён, либо был прерван.

### `.venv/`

- Назначение каталога: локальное виртуальное окружение Python.
- `.venv/pyvenv.cfg`
  - `home = /usr/bin`
  - `include-system-site-packages = false`
  - `version = 3.12.3`
  - окружение создано командой `/usr/bin/python3 -m venv /home/bitplain/brain/.venv`
- Найдены симлинки:
  - `.venv/bin/python`
  - `.venv/bin/python3`
  - `.venv/bin/python3.12`
  - `.venv/lib64`
- Вывод: окружение создано, но его содержимое почти не задействовано в текущем проектном потоке, так как реальный запуск завязан на `scripts/zensical_cli.py` и кэш `.tools/`.

### `.git/`

- Это стандартный не-bare git-репозиторий.
- `.git/config`
  - origin: `https://github.com/bitplain/brain`
  - ветка `main` отслеживает `origin/main`
  - есть `vscode-merge-base = origin/main`
- `.git/HEAD`
  - указывает на локальную ветку `main`.
- `.git/refs/heads/main`
  - локальная ссылка на текущую ветку.
- `.git/refs/remotes/origin/HEAD`
  - ссылка на удалённую ветку по умолчанию.
- `.git/logs/HEAD`, `.git/logs/refs/heads/main`, `.git/logs/refs/remotes/origin/HEAD`
  - reflog-и присутствуют.
- `.git/objects/pack/`
  - pack-файлы присутствуют:
    - `pack-f508ded4da9ea1b85383e9027e8335c6c9eefea8.pack`
    - `pack-f508ded4da9ea1b85383e9027e8335c6c9eefea8.idx`
    - `pack-f508ded4da9ea1b85383e9027e8335c6c9eefea8.rev`
- `.git/hooks/`
  - присутствуют только стандартные sample hooks:
    - `applypatch-msg.sample`
    - `commit-msg.sample`
    - `fsmonitor-watchman.sample`
    - `post-update.sample`
    - `pre-applypatch.sample`
    - `pre-commit.sample`
    - `pre-merge-commit.sample`
    - `pre-push.sample`
    - `pre-rebase.sample`
    - `pre-receive.sample`
    - `prepare-commit-msg.sample`
    - `push-to-checkout.sample`
    - `sendemail-validate.sample`
    - `update.sample`
- Прочие стандартные служебные файлы:
  - `.git/FETCH_HEAD`
  - `.git/ORIG_HEAD`
  - `.git/index`
  - `.git/description`
  - `.git/info/exclude`
  - `.git/packed-refs`
- По признакам это обычный живой клон с минимальной историей и локальными незавершёнными изменениями.

## Что это значит по сути

- Репозиторий всё ещё близок к стартовому шаблону Zensical.
- Главная кастомизация на текущий момент:
  - `docs/init.md` с описанием проекта
  - VS Code-конфигурация для удобного preview/build
  - Python-скрипт локального bootstrap без ручной установки Zensical
- При этом есть следы незавершённой локальной настройки:
  - удалён workflow публикации
  - wheel Zensical докачан не полностью
  - в каталоге лежит внешний `wget-log`
- Содержательно проект пока больше похож на заготовку документационного сайта, чем на наполненную базу знаний.

## Короткий список рисков и наблюдений

- `docs/index.md` и `docs/markdown.md` остаются в значительной степени шаблонными и, вероятно, должны быть либо переработаны, либо заменены реальным контентом.
- `zensical.toml` тоже в основном шаблонный: `site_author` не заполнен, `site_url` не задан, часть кастомизаций не активирована.
- Пустой `.github/workflows/` при удалённом `docs.yml` означает, что автоматическая публикация сайта сейчас локально выключена.
- `.tools/zensical/...download` указывает на незавершённый bootstrap.
- Одновременное наличие `.venv/` и bootstrap-скрипта говорит о двух частично пересекающихся способах локального запуска, что может вносить путаницу.
