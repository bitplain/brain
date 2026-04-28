---
icon: lucide/shield-check
---

<div class="kb-doc kb-doc--cofi" markdown="1">

# Установка ViPNet Client на Windows

<div class="article-intro">
  Короткая памятка по установке ViPNet Client: от запуска инсталлятора до первого окна входа.
</div>

<div class="alert-panel">
  <div class="alert-panel__label">Важно</div>
  <div>
    Для завершения установки потребуется перезагрузка компьютера. После неё ViPNet предложит
    отдельно установить ключи из файла <code>.dst</code>, который нужно заранее получить у администратора.
  </div>
</div>

## Что подготовить

<div class="compare-grid">
  <section class="info-card info-card--soft">
    <h3>Перед запуском</h3>
    <ul>
      <li>Ярлык установщика ViPNet Client на рабочем столе.</li>
      <li>Файл ключей <code>.dst</code> в доступной папке.</li>
      <li>Пароль для первого входа в ViPNet Client.</li>
    </ul>
  </section>
  <section class="info-card">
    <h3>Что произойдёт дальше</h3>
    <ul>
      <li>Сначала установится сам клиент.</li>
      <li>После перезагрузки откроется мастер импорта ключей.</li>
      <li>Затем появится окно первого входа по паролю.</li>
    </ul>
  </section>
</div>

## Быстрая установка

<div class="compact-steps">
  <section class="compact-step">
    <div class="compact-step__media media-frame media-frame--icon">
      <img src="../../assets/instructions/vipnet-client-01.png" alt="Ярлык установщика ViPNet Client на рабочем столе">
    </div>
    <div class="compact-step__body">
      <h3>1. Запустите установщик</h3>
      <p>На рабочем столе найдите ярлык ViPNet Client и откройте его.</p>
      <p class="inline-callout">Если Windows спрашивает подтверждение запуска, разрешите установку.</p>
    </div>
  </section>

  <section class="compact-step">
    <div class="compact-step__media media-frame">
      <img src="../../assets/instructions/vipnet-client-02.png" alt="Окно установки ViPNet Client с лицензионным соглашением">
    </div>
    <div class="compact-step__body">
      <h3>2. Примите лицензию и нажмите «Установить»</h3>
      <p>Поставьте галочку согласия с лицензией и запустите установку кнопкой <strong>Установить</strong>.</p>
      <p>Дальше мастер сам подготовит файлы и установит клиент без дополнительных настроек.</p>
    </div>
  </section>

  <section class="compact-step">
    <div class="compact-step__media media-frame">
      <img src="../../assets/instructions/vipnet-client-04.png" alt="Окно завершения мастера установки ViPNet Client">
    </div>
    <div class="compact-step__body">
      <h3>3. Дождитесь завершения и перезагрузите компьютер</h3>
      <p>Когда мастер сообщит об окончании установки, выберите <strong>Перезагрузить сейчас</strong> или перезагрузите ПК позже вручную.</p>
      <p class="inline-callout">Без перезагрузки импорт ключей и первый вход могут не запуститься корректно.</p>
    </div>
  </section>

  <section class="compact-step">
    <div class="compact-step__media media-frame">
      <img src="../../assets/instructions/vipnet-client-05.png" alt="Окно ViPNet с предложением установить ключи">
    </div>
    <div class="compact-step__body">
      <h3>4. Согласитесь на установку ключей</h3>
      <p>После перезагрузки ViPNet сообщит, что программа ещё не загружена из-за отсутствия ключей.</p>
      <p>Нажмите <strong>Да</strong>, чтобы сразу перейти к мастеру установки ключей.</p>
    </div>
  </section>

  <section class="compact-step">
    <div class="compact-step__media media-frame">
      <img src="../../assets/instructions/vipnet-client-08.png" alt="Мастер установки ключей ViPNet с выбранным файлом .dst">
    </div>
    <div class="compact-step__body">
      <h3>5. Выберите файл ключей <code>.dst</code></h3>
      <p>В мастере установки ключей нажмите <strong>Обзор</strong>, укажите выданный администратором файл <code>.dst</code> и затем нажмите <strong>Установить</strong>.</p>
      <p class="inline-callout">Если нужного файла нет, остановитесь на этом шаге и запросите его у администратора.</p>
    </div>
  </section>
</div>

## Завершение и первый вход

<div class="compare-grid">
  <section class="info-card info-card--soft">
    <div class="media-frame">
      <img src="../../assets/instructions/vipnet-client-09.png" alt="Сообщение об успешной установке ключей ViPNet">
    </div>
    <h3>6. Закройте мастер ключей</h3>
    <p>Если появилось сообщение <strong>Ключи успешно установлены</strong>, нажмите <strong>Закрыть</strong>.</p>
  </section>
  <section class="info-card">
    <div class="media-frame">
      <img src="../../assets/instructions/vipnet-client-10.png" alt="Окно первого входа в ViPNet Client по паролю">
    </div>
    <h3>7. Войдите в ViPNet Client</h3>
    <p>В окне входа оставьте способ аутентификации <strong>Пароль</strong>, проверьте имя пользователя, введите пароль и нажмите <strong>OK</strong>.</p>
  </section>
</div>

<div class="summary-strip">
  <span>Установщик</span>
  <span>Перезагрузка</span>
  <span><code>.dst</code></span>
  <span>Пароль</span>
</div>

</div>
